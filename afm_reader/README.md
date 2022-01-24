# afm_depth_reader
python script to read all .afm files in directory and outputs a csv file 
afm_reader_OC2107A is a specific version of the script that is made for one specific nameing scheme
afm_reader_default is a generic version that uses filename
## Getting Started
Download the Python script and make sure you have python installed.

### Prerequisites
I use anaconda3, however the script should be able to run using pip since the script uses only basic libraries.

### setup
The working directory must be the same folder you have the .afm files in so make sure you move into that directory before running the script.

### testing
I've attatched two example files for the program to read and output into a csv. Feel free to try if it works with the two test cnv files uploaded. I attached the output I get from this script using those two files as "out.csv".

This is my output
```
Station,Cast,Pin,Time,Depth
1,1,1,16:00:40,52
1,1,2,16:08:00,50
1,1,3,16:09:06,40
1,1,4,16:10:06,30
1,1,5,16:11:06,20
1,1,6,16:11:56,10
1,1,7,16:12:23,5
24,2,1,16:07:33,900
24,2,2,16:10:53,798
24,2,3,16:14:00,699
24,2,4,16:17:14,599
24,2,5,16:20:20,499
24,2,6,16:26:41,299
24,2,7,16:30:18,184
24,2,8,16:33:00,98
24,2,9,16:34:13,58
24,2,10,16:35:08,29
```

Enjoy!
-Nathan

readme template from https://gist.github.com/PurpleBooth/109311bb0361f32d87a2#file-readme-template-md
