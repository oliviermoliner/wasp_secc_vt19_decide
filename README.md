[![Build Status](https://api.travis-ci.org/oliviermoliner/wasp_secc_vt19_decide.svg?branch=master)](https://api.travis-ci.org/oliviermoliner/wasp_secc_vt19_decide)
[![Code Style: Black](https://badgen.net/badge/code%20style/black/000)](https://github.com/ambv/black)

# wasp_secc_vt19_decide

As part of a hypothetical anti-ballistic missile system, the ```decide``` function will generate a boolean signal which determines whether an interceptor should be launched based upon input radar tracking information.

The function determines whether a set of conditions called *Launch Interceptor Conditions* are met given the radar information and a set of parameters. Only if all relevant combinations of launch conditions are met will the launch-unlock signal be issued.

The input to the system are:

- **Launch Interceptor Conditions parameters:** parameters for the fifteen LICs
- **Logical Connector Matrix (LCM):** defines which individual LIC’s must be consid- ered jointly in some way. The LCM is a 15x15 symmetric matrix with elements valued ANDD, ORR, or NOT_USED.
- **Preliminary Unlocking Vector (PUV):** represents which LIC actually matters in this particular launch determination.

The following output are generated:

- The fifteen elements of a **Conditions Met Vector (CMV)** will be assigned boolean values true or false; each element of the CMV corresponds to one LIC’s condition.
- The combination of LCM and CMV is stored in the **Preliminary Unlocking Matrix (PUM)**, a 15x15 symmetric matrix.
- Each element of the PUV indicates how to combine the PUM values to form the corresponding element of the **Final Unlocking Vector (FUV)**, a 15-element vector. 
- If, and only if, all the values in the FUV are true, should the launch-unlock signal be generated.

## Installation

To install, clone this repo:

```
git clone https://github.com/oliviermoliner/wasp_secc_vt19_decide.git
```

and then run

```
cd wasp_secc_vt19_decide
pip install -e .
```

## Basic Usage

Here is a basic example:

```python
import math

import decide

# Define the parameters for the Launch Interceptor Conditions
parameters = {
    "length1": 2,
    "epsilon": math.pi / 2,
    "area1": 2,
    "radius1": 1,
    "q_pts": 3,
    "quads": 1,
    "n_pts": 3,
    "dist": 1.5,
}

# Define the Logical Connector Matrix
lcm = [["ORR"] * decide.NUMBER_OF_LICS] * decide.NUMBER_OF_LICS

# Define the Preliminary Unlocking Vector
puv = [
    True,
    True,
    True,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
    False,
]

# Create an instance of the Decide class
decider = decide.Decide(parameters, lcm, puv)

# Run the decide method on a set of points
if decider.decide([[0, 0], [1, 0], [2, 0], [3, 0], [3, 3]]) is True:
    print("Launch")
else:
    print("Do NOT launch")
```

## Contributing

If you wish to contribute, see the [contributing guidelines](CONTRIBUTING.md).


