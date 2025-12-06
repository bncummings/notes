#ifndef HASH_SET_REFINABLE_H
#define HASH_SET_REFINABLE_H

#include <algorithm>
#include <atomic>
#include <cassert>
#include <functional>
#include <mutex>
#include <vector>

#include "src/hash_set_base.h"

template <typename T>
class HashSetRefinable : public HashSetBase<T> {
 public:
  explicit HashSetRefinable(size_t initial_capacity)
      : num_buckets_(initial_capacity) {
    set_size_.store(0);
    resize_generations_.store(0);
    buckets_.resize(initial_capacity);
    mutexes_.store(new std::vector<std::mutex>(initial_capacity));
  }

  bool Add(T elem) final {
    size_t location;
    // Acquire the lock for the relevant bucket to ensure mutual exclusion of
    // operations on that bucket.
    std::unique_lock<std::mutex> lock = acquire(elem, location);

    // If the element is already present, return false.
    if (std::find(buckets_[location].begin(), buckets_[location].end(), elem) !=
        buckets_[location].end()) {
      return false;
    }

    // Otherwise, add the element to the relevant bucket.
    buckets_[location].push_back(elem);
    set_size_.fetch_add(1);

    // Resize if the load factor is exceeded.
    if (static_cast<double>(set_size_.load()) >
        kLoadFactor * static_cast<double>(num_buckets_.load())) {
      lock.unlock();
      Resize();
    }

    return true;
  }

  bool Remove(T elem) final {
    size_t location;
    // Acquire the lock for the relevant bucket to ensure mutual exclusion of
    // operations on that bucket.
    std::unique_lock<std::mutex> lock = acquire(elem, location);

    auto pos =
        std::find(buckets_[location].begin(), buckets_[location].end(), elem);
    // If found, remove the element and return true.
    if (pos != buckets_[location].end()) {
      buckets_[location].erase(pos);
      set_size_.fetch_sub(1);
      return true;
    }

    // Otherwise, return false.
    return false;
  }

  [[nodiscard]] bool Contains(T elem) final {
    size_t location;
    // Acquire the lock for the relevant bucket to ensure mutual exclusion of
    // operations on that bucket.
    std::unique_lock<std::mutex> lock = acquire(elem, location);

    return std::find(buckets_[location].begin(), buckets_[location].end(),
                     elem) != buckets_[location].end();
  }

  [[nodiscard]] size_t Size() const final { return set_size_.load(); }

 private:
  // set_size_ is atomic to allow Size() to be called without locking the mutex.
  std::atomic<size_t> set_size_;
  // num_buckets_ is atomic to allow atomic reads during resizing.
  std::atomic<size_t> num_buckets_;
  /* resize_generations_ is atomic so that threads can atomically check if a
  resize has happened. */
  std::atomic<size_t> resize_generations_;

  std::vector<std::vector<T>> buckets_;
  std::atomic<std::vector<std::mutex>*> mutexes_;

  /* resizing is atomic so that threads can atomically check if a resize is
  happening. */
  std::atomic<bool> resizing;

  const double kLoadFactor = 0.75;

  std::unique_lock<std::mutex> acquire(T elem, size_t& location) {
    for (;;) {
      /* 
      If a resize is happening, we wait until it is finished. 

      Since our implementation of Resize() doesn't call Add() (as in the java implementation),
      we don't need to consider re-entrancy. Hence, we only need to check whether a resize happening,
      and not which thread is performing the resize (we know that the current thread cannot be performing a resize).
      */
      while (resizing.load()) {
      }
      size_t old = resize_generations_.load();

      location = std::hash<T>()(elem) % num_buckets_.load();
      /*
      We acquire the mutex corresponding to the element being accessed using a
      unique lock. This is because we may need to release the lock and try again
      if a resize happens while we are trying to acquire the lock.
      */
      std::unique_lock<std::mutex> lock((*(mutexes_.load()))[location]);

      // Check that no resize has happened or is happening.
      if (!resizing.load() && (resize_generations_.load() == old)) {
        // Success. We keep hold of the lock.
        return lock;
      } else {
        // Failure (someone has resized) so try again.
        lock.unlock();
      }
    }
  }

  void Resize() {
    bool desired = false;
    // Perform a TAS on resizing to ensure only one thread resizes at a time.
    if (resizing.compare_exchange_strong(desired, true)) {
      // Check that we haven't resized already.
      if (static_cast<double>(set_size_.load()) <=
          kLoadFactor * static_cast<double>(num_buckets_.load())) {
        resizing.store(false);
        return;
      }

      // Wait for all operations on buckets to finish.
      // This is done without acquiring the locks to avoid deadlock.
      for (auto& m : *(mutexes_.load())) {
        wait_for_lock(m);
      }

      num_buckets_.store(num_buckets_.load() * 2);

      // Gather all the elements.
      std::vector<T> elems;
      for (auto& bucket : buckets_) {
        for (auto& elem : bucket) {
          elems.push_back(elem);
        }
      }

      std::vector<std::vector<T>> new_buckets;
      new_buckets.resize(num_buckets_.load());

      // Put the elements we found into the new bucket table.
      for (auto& elem : elems) {
        size_t location = std::hash<T>()(elem) % num_buckets_.load();
        new_buckets[location].push_back(elem);
      }

      buckets_ = new_buckets;

      // Create new mutexes for the new buckets.
      std::vector<std::mutex>* new_mutexes =
          new std::vector<std::mutex>(num_buckets_.load());

      /* 
      Atomically swap in the new mutexes and delete the old ones. 
      memory_order_acq_rel ensures that no operations on the old mutexes
      are in progress when we delete them.
      */
      auto* old = mutexes_.exchange(new_mutexes, std::memory_order_acq_rel);
      delete old;

      resize_generations_.fetch_add(1);
      resizing.store(false);
    }
  }

  void wait_for_lock(std::mutex& m) {
    // Waits for a lock to be released without acquiring it.
    while (!m.try_lock()) {
    }
    m.unlock();
  }
};

#endif  // HASH_SET_REFINABLE_H
