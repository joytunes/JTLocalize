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

**Notice** the Localizable.strings encoding is UTF16, Little Endian, with line ending set as LF.  
The different scripts expect & produce the files in this encoding.  
(See appendix 1 on how to convert encoding)  


### JTLocalizable.bundle - The localization bundle

The localize bundle is the directory containing the strings files for the different languages the app is localized to.

For example:

JTLocalizable.bundle  
|&nbsp;&nbsp;&nbsp;+-- en.lproj  
|&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;+-- Localizable.strings  
|&nbsp;&nbsp;&nbsp;+-- ru.lproj  
|&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;+-- Localizable.strings  


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

### The default language directory

The default directory is of the english language, meaning the `en.lprog` directory.  
To change the default language directory:

- Change in the `scripts/genstrings`  

```
DEFAULT_LANG_DIR=en.lproj
``` 
- Change in the `scripts/localization_configuration.py`

```python
DEFAULT_LANGUAGE_DIRECTORY_NAME = "en.lproj"
``` 

### The localization flow

**Remember** The Localizable.strings encoding is UTF16, Little Endian, with line ending set as LF.   
The different scripts expect & produce the files in this encoding.  
(See appendix 1 on how to convert encoding)  

#### The genstrings.sh script

The `genrstrings.sh` scripts wraps iOS `genstrings` script, and add custom internationalized scripts, according to the JTLocalize mechanisms.

`genstrings.sh` script receives two arguments
- <u>The project base directory</u> - The directory in which the app code's lays. The assumption is that the IB files are there (xibs & storyboards).
- <u>The localize bundle path</u> - The path to the localize bundle (containing the strings files for the different languages the app is localized to).
 
The script will produce a new Localizable.strings file in the default language directory.

#### The prepare_for_translation.py

The `prapare_for_translation.py` prepares your different language's localizable files for translation.  
This is done by performing a diff between the strings that are already translated (exist in the language directory), and the new Localizable.strings that was producded by the `genstrings.sh` script.

`prepare_for_translation.py` receives one argument:
- <u>The localize bundle path</u> - The path to the localize bundle (containing the strings files for the different languages the app is localized to).

The script will produce `Localizable.strings.pending` files for each language the app is localized to (the language directory exists),

This is the file containing the strings that should be translated (probably new in the app and yet to be translated).

#### The merge_translations.py

The `merge_translations.py` merges the new translation with the old one for each language the app is localized to.

The translated files should be saved as `Localizable.strings.translated` in the language directory (replacing the `.pending` files).

`merge_translations.py` receives one argument:
- <u>The localize bundle path</u> - The path to the localize bundle (containing the strings files for the different languages the app is localized to).

The script will make the proper merge into the Localizble.strings file for each language.

### Localization Summary

**Remember** The Localizable.strings encoding is UTF16, Little Endian, with line ending set as LF.  
The different scripts expect & produce the files in this encoding.  
(See appendix 1 on how to convert encoding)

- Run `genstrings.sh`
- Run `prepare_for_translation.py`
- Translate the `Localizable.strings.pending` files in the different languages directories (convert encoding if needed, see Appendix 1).
- Save the tanslated file in the language directory under `Localizable.strings.translated` (convert encoding if needed, see Appendix 1).
- Run `merge_translations.py`

## Appendix 1 - How to convert Localizable.strings to proper encoding
```
iconv -f utf-8 -t utf-16 Localizable.strings > Localizable.new.strings 
```
to convert utf-8 file to the format we use in the scripts.

```
iconv -f utf-16 -t utf-8 Localizable.strings > Localizable.new.strings
```
for the opposite effect. 

