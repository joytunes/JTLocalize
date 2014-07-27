JTLocalize
==========

iOS localization framework.

The framework supplies common UI elements (UIButton, UILabel, UITextField) with integrated internationalization options,
and scripts which simplify the localization flow.

Using JTLocalize you can easily complete the localize flow for your application continuously.

## Internationalization in iOS

## The Localizable.strings file
The Localizable.strings file is the file used by iOS to store and retrieve strings used within the app, for each supported language.

The files contains entries with the following format:
    /* Comment */
    key = value

For proper internationalization two main things need to be taken care of:                                               
 27 - Extracting the string for localization (key and comment)                                                              
 28 - Submitting the localized string in the code after translation. 

##  The Localizable.strings file
The file 



## How to get started

## Architecture & Implementation
The framework provides solutions for both internationalization and localization.

Internationalization is done using custom objective-c classes and simple markings.

For proper internationalization two main things need to be taken care of:
- Extracting the string for localization (key and comment)
- Submitting the localized string in the code after translation.

For extracting the strings the framework provides the following markings:
- For UILabel, UIButton, UITextField
user label

## Internationalize UI Elements

### UILabel
In order to internalionalize your UILabel, simply 

