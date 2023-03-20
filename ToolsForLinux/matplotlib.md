# [Matplotlib](https://matplotlib.org/)
--
Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python. Matplotlib makes easy things easy and hard things possible. 


## How to fix "Times New Roman" font in Linux 

Step 1: Install this font on your computer:

```shell
sudo apt install msttcorefonts -qq
rm ~/.cache/matplotlib -rf
```

Step 2: If texts in the generated figures are bolded, you can copy the following to your code and run again. 
The following code only need once. 

```python
import matplotlib
del matplotlib.font_manager.weight_dict['roman']
matplotlib.font_manager._rebuild()
```