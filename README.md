# Python hackathon
This documents contains description of the challenge, its explanation
as well as referent software implementation.

# Modeling the challenge

# Explain the challenge

# Solve the challenge --- the implementation part
Firstly, clone this project:

``` shell
git clone <path_to_this_repo>
```

Then make a fresh [virtualenv](https://virtualenv.pypa.io/en/stable/)
and activate it. After that, install all required modules into active
virtualenv using:

``` shell
cd <dir_where_this_repo_is_cloned>
pip install -r requirements.txt
```

Then run the proposed solution with:

``` shell
python3 run_solution.py
```

Now run the framework part to start getting data from it:

``` shell
python3 run_framework.py
```

Visualization is by default available at
[http://localhost:8000/viz.html](http://localhost:8000/viz.html). All
these steps are also available as single script `run.py` that can be
run using:

``` shell
python3 run.py
```

or

``` shell
./run.py
```

*This script will run solution then framework and as the very last
step it will open your default system browser at visualization page.*

**All the available framework options are placed and explained in
params.conf**

**Before you start working on your solution consider the proposed
solution architecture.**

**Proposed solution as well as framework requires Python 3.**

## Typhoon framework
Typhoon framework is given as a Python script that could be run using:

``` shell
./framework.py
```

Or:

``` shell
ptyhon framework.py
```

Framework starts emitting data in the form of `DataMessage`
(`DataMessage` alongside with other offered utilities is placed in the
`utils` module) after time lapse specified in `params.conf`.

## Proposed solution
Communication between Typhoon framework and the solution is abstracted
through the `Control` class from `utils` module. Control class has
`get_data` and `push_results`. First method returns Python generator
that produces data sent by the framework encapsulated into
`DataMessage` objects. Second is aimed to send data back to the
Typhoon framework when it is ready, data that is sent should be
encapsulated into `ResultsMessage` object. Proposed solution that
depicts usage of the `Control` class is given below:

``` python
def worker(msg: DataMessage) -> ResultsMessage:
    print('Worker doing its job, message is {} ...' \
          .format(msg))
    return ResultsMessage(msg, 0, 0, 0)

if __name__ == '__main__':
    cntrl = Control()

    for data in cntrl.get_data():
        cntrl.push_results(worker(data))
```

One can run proposed solution using:

``` shell
./run_solution.py
```

Or:

``` shell
python run_solution.py
```
