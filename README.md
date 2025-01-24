# Signal Equalizer

## Overview  
Signal Equalizer is a versatile tool widely used in the music and speech industry. It also finds applications in biomedical fields, such as hearing aid development and abnormality detection.

## Description  
This project involves developing a desktop application capable of:  
1. Opening a signal file.  
2. Allowing users to modify the magnitude of specific frequency components using sliders.  
3. Reconstructing and playing back the modified signal.  

The application supports multiple operational modes with varying use cases.


## Features  

### **General Functionality:**  
- **Cine Signal Viewers**:  
  - Two linked signal viewers (for input and output signals) with full functionality:  
    - Play/Pause/Stop.  
    - Speed Control.  
    - Zoom, Pan, and Reset options.  
    - Linked scrolling and zooming for synchronous viewing.  

- **Spectrograms**:  
  - Displays spectrograms for both input and output signals.  
  - Reflects real-time changes when sliders are adjusted.  
  - Option to toggle show/hide for spectrograms.  

- **Fourier Transform Visualization**:  
  - Displays frequency ranges in linear and audiogram scales.  
  - Users can switch scales without interrupting functionality.  

---

## Modes  

### **1. Uniform Range Mode**  
- Divided the total frequency range in a synthetic signal into 10 equal parts.  
- Each part is controlled by one slider.

---

### **2. Music and Animal Sounds Mode**  
- Combines functionality for music and animal sound signals:  
  - **Music Mode**:  
    - Controls the magnitude of specific instruments and animal sounds in a mixed music-animal signal.  
    - Ability to cancel **3 instruments** and **3 animals** entirely.  
- Sliders can control specific frequency ranges or combinations of ranges.

---

### **3. Vocals and Instruments Mode**  
- Processes music signals containing vocals and instruments:  
  - Allows users to control the magnitude of individual vocals and instruments.    
  - Ability to cancel **2 vocals** and **2 instruments**.  

---

### **4. Wiener Filter Mode**  
- Applies a Wiener filter to remove noise from a song.  
- Useful for enhancing noisy audio recordings.  

---

## How to Switch Between Modes  
- Users can easily switch between modes using combobox.  
- UI dynamically updates slider captions and count based on the selected mode.



