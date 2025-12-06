#ifndef HASH_SET_COARSE_GRAINED_H
#define HASH_SET_COARSE_GRAINED_H

#include <algorithm>
#include <atomic>
#include <cassert>
#include <functional>
#include <mutex>
#include <vector>

#include "src/hash_set_base.h"

template <typename T>
class HashSetCoarseGrained : public HashSetBase<T> {
 public:
  explicit HashSetCoarseGrained(size_t initial_capacity)
      : num_buckets_(initial_capacity) {
    set_size_.store(0);
    buckets_.resize(initial_capacity);
  }

  /*
    In Add, Remove, and Contains, we acquire the mutex using a scoped lock.
    The scoped lock releases the mutex automatically when the lock goes out of
    scope, and it will lock the mutex for the entire duration of the operation.
    This means that only one thread at a time can perform any operation on the
    hash set.
  */

  bool Add(T elem) final {
    std::scoped_lock<std::mutex> lock(mutex_);
    size_t location = std::hash<T>()(elem) % num_buckets_;
    // If the element is already present, return false.
    if (std::find(buckets_[location].begin(), buckets_[location].end(), elem) !=
        buckets_[location].end()) {
      return false;
    }
    // Otherwise, add the element to the relevant bucket.
    buckets_[location].push_back(elem);
    // Resize if the load factor is exceeded.
    if (static_cast<double>(set_size_.load()) >
        kLoadFactor * static_cast<double>(num_buckets_)) {
      Resize();
    }
    set_size_.fetch_add(1);
    return true;
  }

  bool Remove(T elem) final {
    std::scoped_lock<std::mutex> lock(mutex_);
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
    std::scoped_lock<std::mutex> lock(mutex_);
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
  std::mutex mutex_;

  const double kLoadFactor = 0.75;

  void Resize() {
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

#endif  // HASH_SET_COARSE_GRAINED_H
