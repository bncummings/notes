#ifndef HASH_SET_STRIPED_H
#define HASH_SET_STRIPED_H

#include <algorithm>
#include <atomic>
#include <cassert>
#include <functional>
#include <mutex>
#include <vector>

#include "src/hash_set_base.h"

template <typename T>
class HashSetStriped : public HashSetBase<T> {
 public:
  explicit HashSetStriped(size_t initial_capacity)
      : num_buckets_(initial_capacity),
        num_mutexes(initial_capacity),
        mutexes(initial_capacity) {
    set_size_.store(0);
    buckets_.resize(initial_capacity);
  }

  bool Add(T elem) final {
    size_t mutex_index = std::hash<T>()(elem) % num_mutexes;
    /*
      We acquire the mutex corresponding to the element being added using a
      unique lock. We use a unique lock instead of a scoped lock because we may
      need to release the lock before the end of the function (the case where we
      need to resize the hash set).
    */
    std::unique_lock<std::mutex> lock(mutexes[mutex_index]);
    size_t location = std::hash<T>()(elem) % num_buckets_;
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
        kLoadFactor * static_cast<double>(num_buckets_)) {
      lock.unlock();
      Resize();
    }
    return true;
  }

  bool Remove(T elem) final {
    size_t mutex_index = std::hash<T>()(elem) % num_mutexes;
    /*
      We acquire the mutex corresponding to the element being removed using a
      scoped lock. There is no need to release the lock before the end of the
      function in this case. Since we don't need this behaviour, a scoped lock
      is preferred for efficiency.
    */
    std::scoped_lock<std::mutex> lock(mutexes[mutex_index]);
    size_t location = std::hash<T>()(elem) % num_buckets_;
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
    size_t mutex_index = std::hash<T>()(elem) % num_mutexes;
    /*
      Similar to Remove, we use a scoped lock to acquire the mutex corresponding
      to the element being checked since we don't need to release the lock
      before the end of the function.
    */
    std::scoped_lock<std::mutex> lock(mutexes[mutex_index]);
    size_t location = std::hash<T>()(elem) % num_buckets_;
    return std::find(buckets_[location].begin(), buckets_[location].end(),
                     elem) != buckets_[location].end();
  }

  [[nodiscard]] size_t Size() const final { return set_size_.load(); }

 private:
  // set_size_ is atomic to allow Size() to be called without locking the mutex.
  std::atomic<size_t> set_size_;
  size_t num_buckets_;
  std::vector<std::vector<T>> buckets_;

  const size_t num_mutexes;
  std::vector<std::mutex> mutexes;

  const double kLoadFactor = 0.75;

  void Resize() {
    /*
      We acquire all mutexes using unique locks so that other threads can't do
      operations on the hash set while we are resizing.

      Unique locks are used here so that we can construct the locks in a loop
      and put them in a vector. We can't do this with scoped locks because
      scoped locks need to be constructed as soon as they are declared.
    */
    std::vector<std::unique_lock<std::mutex>> locks;

    for (auto& m : mutexes) {
      locks.emplace_back(m);
    }

    // Check that no other thread has resized while we were waiting for the
    // locks.
    if (static_cast<double>(set_size_.load()) <=
        kLoadFactor * static_cast<double>(num_buckets_)) {
      return;
    }

    num_buckets_ *= 2;

    // Gather all the elements.
    std::vector<T> elems;
    for (auto& bucket : buckets_) {
      for (auto& elem : bucket) {
        elems.push_back(elem);
      }
    }

    std::vector<std::vector<T>> new_buckets;
    new_buckets.resize(num_buckets_);

    // Put the elements we found into the new bucket table.
    for (auto& elem : elems) {
      size_t location = std::hash<T>()(elem) % num_buckets_;
      new_buckets[location].push_back(elem);
    }

    buckets_ = new_buckets;
  }
};

#endif  // HASH_SET_STRIPED_H
