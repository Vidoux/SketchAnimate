# Get Started with SketchAnimate

Welcome to SketchAnimate! This guide will walk you through setting up SketchAnimate on your system and writing your first animation code step by step.

## Prerequisites

Before you start, ensure you have the following installed:

    Linux environnement on your computer (Windows tutorial is coming soon)
    Python 3.7 or later
    ANTLR 4.7.2 or later (for generating parsers from grammar files)

## Step 1: Downloading SketchAnimate

Start by downloading the last release of sketchAnimate. 
You can also download last development version but be aware that you may encounter bugs. ```git clone https://github.com/yourusername/SketchAnimate-main.git```

## Step 2: Setting Up Your Environment

It's recommended to use a virtual environment for Python projects. Create and activate one with:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

Next, install the required dependencies:

```bash
pip install -r requirements.txt
```

## Step 3: Running Your First Animation

Download the example svg here: [example.svg](..%2Fassets%2Fexample.svg)<br>
Let's create a simple animation script. Create a file named first_animation.ska in the project root with the following content:
```ska
// first_animation.ska
main {
    loadSVG("./example.svg");

    moveTo(circle1, 0, 500, 100, 100); // Move to (100, 100) over 500ms
    rotate(square1, 200, 500, 80); // rotate square1 to 80°, starting at 200ms and during 500ms
    exportAnimation(gif,"./export/animation.gif");

}
```

This script loads an SVG, creates a group with two shapes (circle1 and square1), and moves the group to a new position.


## Step 4: Running the Animation

To run your animation, use the sketchanimate_cli tool:

```bash
python src/cli/sketchanimate_cli.py run first_animation.ska
```

This will execute your animation script. If everything is set up correctly, you'll see your animation come to life!


## What's Next?

Congratulations on running your first animation with SketchAnimate! Here are a few suggestions on what to explore next:

1. [x] Experiment with different animation actions like rotate, changeColor, and setVisible.
2. [x] Try creating more complex animations using sequences.
3. [x] Explore the SketchAnimate documentation to learn more about its capabilities. (Not yet available, please feel free to contribute)

Happy animating!
