# generic-decorators

Generic Python Decorators for use in any project.

## Install

`generic-decorators` is released to public PyPI - [generic-decorators](https://pypi.org/project/generic-decorators/). It can be installed using this command:
```
pip install generic-decorators
```

## Decorators

### `make_parallel` 

**Summary**: runs function in parallel instead of sequencial for loop.

**Example**

Parallel trigger of functions `sample_function` with 1 param `list_of_post_ids`
using `make_parallel` decorator and equivalent sequential trigger using `for loop`.

```python
def parallel_function_trigger():
    list_of_post_ids = list(range(1, 20))
    return make_parallel(sample_function)(list_of_post_ids)

#equivalent sequencial version
def serial_function_trigger():
    list_of_post_ids = list(range(1, 20))

    # Serial way of calling the function
    results = []
    for post_id in list_of_post_ids:
        res = sample_function(post_id)
        results.append(res)
    return results

```

You can use below [timing](timing) decorator to compare time of above parallel 
and sequential versions.

### `timing` 

**Summary**: calculate and print how much time function processing took.

**Example**

```python
@timing
def sleep_n_seconds(n: int):
    time.sleep(n)

sleep_n_seconds(5)
```

It should print something like this (time can differ):
```
func:'sleep_n_seconds' args:[(5,), {}] took: 5.0047 sec
```

