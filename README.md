JTLocalize
==========

iOS localization framework.

The framework supplies common UI elements (UIButton, UILabel, UITextField) with integrated IB internationalization options,
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

For **UIButton**, **UILabel**, **UITextField** - Each one of them has a corresponding class in the JTLocalize framework (**JTButton**, **JTLabel**, **JTTextField**).
Use them (The JTLocalize classes) as the custom classes of the UI element. 
This classes use the proper localized string when setting the text.

The next thing you need to do, is to make sure this string will be extracted to the Localizable.strings file.
To do this, simply **change the element's userLabel, using the JTL_ prefix**. This prefix is respected by our localization scripts for string extaction.
The rest of the string in the userLabel (after the JTL_ prefix) will be used as the comment of the localizaation entry in the Localizable.strings files.

For DTCoreText elements (DTAttributedLabel) - This is illustrated in the example project, to avoid DTCoreText dependency. 
If you want to use them (and internationalize them), **add a keypath named htmlString with an html string value**.
**In this html string value, simply put JTL("Key", "Comment") wherever you would a localized string value**.

The example project also illustrtes how to include internationzalized links in your project.   

#### Internationalize strings in the code

For internalizing strings in the code, use the JTLocalizedString() macro: 
```objective c
NSString *localizedString = JTLocalizedString("Some string", "The Strings context for translation")
```

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

