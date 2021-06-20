## Mapping arbitrary graphs to equations using Discrete Fourier Transform. Using Turtle as a visualizer and animator.

### Run
`python3 main.py {hunter, scene, fairy}`
See `python3 main.py -h` for more details.

See SVG files in resources for sample of the original image.

### Turtle and animation.

We use turtle as a visualizer for visualizing the entire curve. Every closed loop is a single curve. We can hence get a single equation for the entire curve. The curve is animated as if someone is drawing the curve by hand. This is generic and works with most SVG files with no additional overhead.

<img src="demo.png">

### Representation of 2D coordinates.
We use a complex number (inbuilt support from python) for this.

### Parsing subset of SVG

First, we create a partial SVG (see references) command parser able to parse absolute commands (L, C, M, V, H, Z).

The most interesting of them being the cubic bezier curve, which is a parametric curve taking values from 0-1.

<img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/a4a840bf8e22c383e6841ca3cb01563b4632ad6f">

We then calculate values of different points in the curve, as well as the length of the curve.

This requires us to integrate as well as differentiate the bezier curve over the interval [0,1]

The derivative being the simple equation.

<img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/bda9197c2e77c17d90839b951cb0035d79c8d417">

Since calculating the integral cannot be done easily, we use a numerical approximation to calculate the integral.


## Discrete Fourier Series
From the samplers created for the above curves, we generate a single equation for the entire curve.

We calculate the coefficients for the fourier series using the following formula.  Integrating the equation is not simple (We could not find a simple integral. Therefore, we use a numerical approximation.


<img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/18b0e4c82f095e3789e51ad8c2c6685306b5662b">

### Applications
Known Applications:
- Lossy data compression (JPEG for example uses the discrete cosine transform function to efficiently compress lossily)
- Fast multiplication algorithms using FFT.
- Spectral analysis
- Signal processing.
- See (<a href="https://en.wikipedia.org/wiki/Discrete_Fourier_transform#Applications"> Applications </a> for more details)

### References
<a href="https://en.wikipedia.org/wiki/Discrete_Fourier_transform"> Discrete Fourier Transform</a>:  In mathematics, Fourier analysis is the study of the way general functions may be represented or approximated by sums of simpler trigonometric functions.

<a href="https://en.wikipedia.org/wiki/Scalable_Vector_Graphics"> Scalable Vector Graphics (SVG) </a> is an Extensible Markup Language (XML)-based vector image format for two-dimensional graphics with support for interactivity and animation.


<a href="https://en.wikipedia.org/wiki/B%C3%A9zier_curve"> Bezier curves </a> A Bézier curve is a parametric curve used in computer graphics and related fields.