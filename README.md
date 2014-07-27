JTLocalize
==========

iOS localization framework.

The framework supplies common UI elements (UIButton, UILabel, UITextField) with integrated internationalization options,
and scripts which simplify the localization flow.

Using JTLocalize you can easily complete the localize flow for your application continuously.

## Internationalization

### Internationalization in iOS

#### The Localizable.strings file
The Localizable.strings file is the file used by iOS to store and retrieve strings used within the app, for each supported language.

The files contains entries with the following format:
```
/* Comment */
Key = Value;
```

Comment - The context of the string for translation.
Key - The string to translate.
Value - The translated value.

### Internationalize using JTLocalize

For proper internationalization two main things need to be taken care of:                                               
- Extracting the string for localization (Key & Comment).                                                             
- Using the localized values after translation. 

#### Internationalize UI Elements

- For UIButton, UILabel, UITextField - Each one of them has a corresponding class in the JTLocalize framework (JTButton, JTLabel, JTTextField).
Use them as the custom classes of the UI element. This is for the second part of internationalization - using the localized string.

The next thing you need to do, is to make sure this string will be extracted to the Localizable.strings file.
To do this, simply change the element's userLabel, using the JTL_ prefix. The rest of the string in the userLabel (after the JTL_ prefix) will be used as the comment of the localizaation entry in the Localizable.strings files.
 


Simply use the JTL_ prefix in the userLabel of the element. The string after the prefix will be used as a comment in the Localizabe.strings file.
- For DTCoreText elements (DTAttributedLabel) - This is illustrated in the example project, to avoid DTCoreText dependency. 
Use htmlString as a keypath and put JTL("Key", "Comment") in the value 


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

