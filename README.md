
# Animated Visualization of Running Data with Intense Wind Effects

This project visualizes the speed and power data of two runners, Carla and Colo, using an animated video that includes dynamic effects such as glow, real-time annotations, and intense wind effects. The final video is created using Python, Pygame, and MoviePy, and includes a background soundtrack.

## Requirements

To run this code, you will need the following:

### Python Version
- Python 3.7 or higher

### Libraries
The following Python libraries are required:

- `pygame`: For creating the animation and handling the graphics.
- `pandas`: For handling the data files and performing calculations.
- `moviepy`: For compiling the animation frames into a video and adding the soundtrack.

You can install the required libraries using `pip`:

```bash
pip install pygame pandas moviepy
```

### Data Files
You need the following CSV files containing the running data:

- `StrydCarla3k.csv`: Contains data for Carla.
- `StrydColo3k.csv`: Contains data for Colo.

These files should include the following columns:
- `pace`: Pace in min/km
- `stryd`: Power output in watts
- `wind`: Wind intensity

### Media Files
- `chico.png`: Sprite image for Colo.
- `chica.png`: Sprite image for Carla.
- `wind.png`: Image representing the wind effect.
- `sonido.mp3`: Audio file for the background soundtrack.

### Folder Structure
Place all the necessary files in the same directory as the script:

```
/your_project_directory/
    ├── StrydCarla3k.csv
    ├── StrydColo3k.csv
    ├── chico.png
    ├── chica.png
    ├── wind.png
    ├── sonido.mp3
    ├── your_script.py
```

## How to Run

1. **Ensure all required libraries are installed.**
   - Use the `pip install` commands listed above.

2. **Place all required files in the correct directory structure.**

3. **Run the script:**
   - Execute the script using Python:
   ```bash
   python your_script.py
   ```

4. **Output:**
   - The script will generate a video file named `carla_colo_animation_with_sound.mp4` in the same directory, visualizing the speed and power data of both runners with added wind effects.

## Notes

- Ensure that the data in the CSV files is correctly formatted and that the file paths to the media files are accurate.
- The animation loop will continue until all frames are processed, and the video will be created with a frame rate of 60 FPS.
