# Status Screen for Laser Labs  

Based on Taurus status screen to display crucial parameters in control room of SXR Lab. The need of a second status screen to display different parameters in the lab motivated the refactoring of the satus screen code.

## Structure and Use

```statusscreen/  
|--main.py  
|--core/  
    |--window.py  
    |--panel.py  
    |--utils.py  
|--styles/  
    |--mbi-styles.qss  
    |--fonts/  
    |--logos/  
|--configs/  
    |--lab.yaml  
    |--lab_screen01.yaml  
    |--lab_screen02.yaml  
```
### Development  

- main.py builds the Taurus Application  
- window.py builds the main window consisting of different panels  
- panel.py used to define different panels to align multiple properties to display  

### Goal  

- use lab.yaml file to define lab specific properties  
- use lab_screenXX.yaml to define which properties to display at a specific status screen inside the lab  