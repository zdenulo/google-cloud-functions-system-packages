# Examples of using system and custom programs in Google Cloud Functions

## List of cloud functions to demonstrate possibilities to use Unix and compiled programs in Cloud Functions:
1. cf_ascii - using figlet [http://www.figlet.org/](http://www.figlet.org/) compiled C program which converts text to ASCII text. Input request with parameter contains 
text which should be converted to ASCII    
2. cf_pdf2png - using provided ghostscript program to convert PDF file to PNG images (1 page -> 1 image)  
3. cf_system - executing various system commands to explore system within Cloud Functions, like displaying all binaries,
executing commands.   

More information can be found in this article [Using system packages and custom binaries in Google Cloud Functions.](https://www.the-swamp.info/blog/google-cloud-functions-system-packages/)
