JTLocalize
==========

iOS localization framework.

The framework supplies common UI elements (UIButton, UILabel, UITextField) with integrated IB internationalization mechanisms,
and scripts respecting these mechanisms which simplify the localization flow.

Using JTLocalize you can easily complete the localize flow for your application continuously.

## Internationalization

Internationalization is done using custom objective-c classes and simple marking mechanisms.

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

### JTLocalizable.bundle - The localization bundle

The localize bundle is the directory containing the strings files for the different languages the app is localized to.

For example:

JTLocalizable.bundle <br/>
|   +-- en.lproj <br/>
|   |   +-- Localizable.strings <br/>
|   +-- ru.lproj <br/>
|   |   +-- Localizable.strings <br/>


### Internationalize using JTLocalize

For proper internationalization two main things need to be taken care of:                                               
- Extracting the string for localization (Key & Comment).                                                             
- Using the localized values after translation. 

#### Internationalize UI Elements

Internationalization of UI elements works for both xibs and storyboad files.

For `UIButton`, `UILabel`, `UITextField` - Each one of them has a corresponding class in the JTLocalize framework (`JTButton`, `JTLabel`, `JTTextField`).
Use them (The JTLocalize classes) as the **Custom Class**es of the UI element. 
This classes use the proper localized string when setting the text.

The other thing you need to do, is to make sure this string will be extracted to the Localizable.strings file.
To do this, simply **change the element's userLabel, using the `JTL_` prefix**. 
This prefix is respected by our localization scripts for string extaction.
The rest of the string in the userLabel (after the `JTL_` prefix) will be used as the comment of the localizaation entry in the Localizable.strings files.

For `DTCoreText` elements (`DTAttributedLabel`) - This part is illustrated in the example project, to avoid `DTCoreText` dependency. 
If you want to use them (and internationalize them), add a **keypath named htmlString** with an html string value.
In this html string value, simply put `JTL("Key", "Comment")` wherever you would a localized string value.

The example project also illustrates how to include **internationzalized links** in your project.   

#### Internationalize strings in the code

For internalizing strings in the code, use the JTLocalizedString() macro: 
```objective-c
NSString *localizedString = JTLocalizedString("Some string", "The Strings context for translation")
```

## Localization

The JTLocalize framework provides scripts that integrate with the internationalization mechanisms, and simplify the localization flow.

### The genstrings.sh script

The `genrstrings.sh` scripts wraps iOS `genstrings` script, and add custom internationalized scripts, according to the JTLocalize mechanisms.

`genstrings.sh` scripts accepts two arguments
- The prject base directory - The directory in which the app code's lays. The assumption is that the IB files are there (xibs & storyboards).
- The localize bundle path - The path to the localize bundle (containing the strings files for the different languages the app is localized to).
 



