# SketchAnimate

<img alt="SketchAnimate Logo" height="auto" src="assets/Logo1.png" width="200" style="display: block; margin: 0 auto"/>

SketchAnimate is an open-source project aimed at developing a Domain Specific Language (DSL) for animating technical drawings using Scalable Vector Graphics (SVG) files. This DSL is designed to empower users to animate elements within technical drawings, offering control over movement, visibility, size, color changes, and fading, among other capabilities.

## Kanban Board

We manage our project tasks and development progress using a Kanban board. You can view and track our work on the [SketchAnimate Kanban board](https://tree.taiga.io/project/vidoux-sketchanimate/kanban).

## Table of Contents

- [Features](#features)
- [Installation and Setup](#installation-and-setup)
  - [Prerequisites](#prerequisites)
  - [Installing SketchAnimate](#installing-sketchanimate)
  - [Compiling the DSL Grammar](#compiling-the-dsl-grammar)
  - [Using SketchAnimate additional Tools](#using-sketchanimate-additional-tools)
  - [Getting Started with the SketchAnimate Language](#getting-started-with-the-sketchanimate-language)
- [Usage](#usage)
- [Technical Stack](#technical-stack)
- [Similar or related projects](#similar-or-related-projects)
- [References](#references-)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Animation Library**: A comprehensive library to animate SVG elements, offering a range of animation effects such as movements, fades, and color changes.
- **Custom DSL**: SketchAnimate introduces a custom-designed DSL that supports both imperative and object-oriented paradigms, making it flexible for users to define complex animations.
- **User-Friendly Tools**: Besides the core animation functionalities, the project includes tools for adding IDs to SVG elements and a GUI fto identify ids of elements in SVGs.
- **Documentation**: Detailed documentation, including a user guide and a DSL reference, provides all the information needed to get started with animating technical drawings.

## Installation and Setup

### Prerequisites

 Before installing SketchAnimate, ensure you have the following installed: 

- Python 3.8 or newer 

- Pip (Python package installer)

- ANTLR 4.7.2 or newer (for compiling the DSL grammar)  

### Installing SketchAnimate

1. **Clone the repository:**
   
   ```bash
   git clone https://github.com/Vidoux/SketchAnimate.git
   cd SketchAnimate-main
   ```

2. **Install Python dependencies:**
   
   ```bash
   pip install -r requirements.txt
   ```

### Compiling the DSL Grammar

SketchAnimate uses ANTLR for its custom DSL. Here's how to generate the compilation toolchain

1. **Install ANTLR4**
   
   ```bash
   pip install antlr4-tools
   ```

2. **Navigate to the grammar directory:**
   
   ```bash
   cd src/language/codegen
   ```

3. **Compile the grammar:** 
   
   ```bash
   antlr4 -Dlanguage=Python3 SketchAnimateImperativeParadigm.g4 -o ./antlr_build -visitor
   ```

### Using SketchAnimate additional Tools

SketchAnimate includes tools for adding IDs to SVG elements and a GUI to identify ids of elements in SVGs.

##### Add IDs to SVG Elements

To add IDs to your SVG elements for easier reference in animations:

1. **Navigate to the tools directory:**
   
   ```bash
   cd src/tools
   ```

2. **Run the ID adding tool:**
   
   ```bash
   python Add_ids_svg.py <path_to_your_svg>
   ```

##### Identify ids in SVGs

To use the GUI for creating and managing animations:

1. **Navigate to the tools directory**
   
   ```bash
   cd src/tools
   ```

2. **Launch the tool:**
   
   ```bash
   python SVG_ClickID_Viewer.py <path_to_your_svg>
   ```

### Getting Started with the SketchAnimate Language

To create your first animation script using the SketchAnimate DSL:

1. **Write Your Animation Script**: Use your favorite text editor to write the animation script. Save it with a `.ska` extension.

2. **Compile Your Animation Script**: Use the SketchAnimate compiler to compile your script and apply the animations to your SVG.
   
   ```bash
   python .py <your_script>.ska
   ```
   
// TODO
## Usage

Begin by reading the [user guide](docs/user-guide.md) for detailed instructions on using SketchAnimate and scripting animations with the DSL. The guide covers everything from basic animations to more complex scenarios.

## Technical Stack

SketchAnimate is built using a combination of technologies and frameworks to provide a robust and user-friendly experience for animating technical drawings.

- **Python**: The core language used for developing the project, including the animation library and DSL processing.
- **ANTLR**: Utilized for defining and processing the custom DSL, enabling complex language constructs for animation scripting.
- **SVG**: Scalable Vector Graphics format is at the heart of SketchAnimate, serving as the basis for the technical drawings that are animated.
- **Tkinter**: For the graphical user interface components, allowing users to interact with the tool in a more intuitive way.

This stack was chosen for its flexibility, ease of use, and the rich set of features it offers for both language processing and graphical manipulation.


## Similar or related projects

Here is a list of differnts projects about animating svg or working around animation: 

- **[Lottie](https://github.com/airbnb/lottie-web)**: Lottie is an open-source library from AirBnB that enables the creation and playback of vector animations. It's particularly well-suited for integrating animations into web and mobile applications.

- **[Raphael.js](https://github.com/DmitryBaranovskiy/raphael)**: Raphael.js is a JavaScript library that simplifies the creation of animations and vector graphics. It provides features for manipulating SVG elements and creating interactive visualizations.

- **[Snap.svg](https://github.com/adobe-webplatform/Snap.svg)**: Snap.svg is a JavaScript library similar to Raphael.js, designed for manipulating and animating SVG elements. It offers an efficient way to create SVG-based animations and interactions.

- **[Rive](https://github.com/rive-app/rive)**: Rive is an open-source animation library that allows you to create interactive animations for the web and applications. You can create vector animations and integrate them into your projects.

## References 

- "Crafting Interpreters: A Handbook for Making Programming Languages" written by Robert Nystrom
- website: [https://craftinginterpreters.com/](https://craftinginterpreters.com/)
  

## Contributing

Contributions are welcome! Whether you're looking to fix bugs, add new features, or improve documentation, please read our [contribution guidelines](CONTRIBUTING.md) for more information on how to contribute.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

SketchAnimate is a collaborative project developed by engineering students as part of their end-of-study requirements. We extend our gratitude to Jean-Christophe Le Lann for supervising the project and to all contributors and users for their valuable feedback and contributions.


For any questions or support, please [open an issue](https://github.com/your-username/SketchAnimate/issues) or [reach out by mail](mailto:tanguy.vidal@ensta-bretagne.org). We'd love to hear from you!
