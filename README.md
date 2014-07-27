JTLocalize
==========

iOS localization framework.

The framework supplies common UI elements (UIButton, UILabel, UITextField) with integrated IB internationalization mechanisms,
and scripts respecting these mechanisms which simplify the localization flow.

JTLocalize solves two of the major pains in iOS localization:
- No need for separate strings file per storyboard/xib. Only one file to maintain.
- Continuous translation intergration simplified.  
No need to localize everything again, just send the diff and merge it back. 

### Internationalize

Internationalization is done using custom objective-c classes and simple marking mechanisms.

#### Internationalize UI Elements

Internationalization of UI elements works for both xibs and storyboad files.

In order to internationalize UI element (`UIBotton`,`UILabel`,`UITextField`):
- Use the corresponding class in the JTLocalize framework (`JTButton`, `JTLabel`, `JTTextField`) as the <b>Custom Class</b>es of the UI element. 
These classes use the proper localized string when setting the text.

- Change the element's userLabel, using the `JTL_` prefix. 
This prefix is respected by our localization scripts for string extaction.
The rest of the string in the userLabel (after the `JTL_` prefix) will be used as the comment of the localizaation entry in the Localizable.strings files.

To internationalize `DTCoreText` elements (`DTAttributedLabel`) see the illustration in the example project.
(The reason this is only illustrated is to avoid `DTCoreText` dependency). 

If you want to use them (and internationalize them), add a **keypath named htmlString** with an html string value.
In this html string value, simply put `JTL("Key", "Comment")` wherever you would a localized string value.

The example project also illustrates how to include **internationzalized links** in your project.   

#### Internationalize strings in the code

For internalizing strings in the code, simply use the NSLocalizedString() macro (exactly like the ordinary way): 
```objective-c
NSString *localizedString = NSLocalizedString("Some string", "The Strings context for translation")
```

### Localize

The JTLocalize framework provides scripts that integrate with the internationalization mechanisms, and simplify the localization flow.


### The localization flow

- Run `scripts/genstrings.sh`
- Run `scripts/prepare_for_translation.py`
- Translate the `Localizable.strings.pending` files in the different languages directories  
(convert encoding if needed, see appendix).
- Save the tanslated file in the proper language directory under `Localizable.strings.translated`  
(convert encoding if needed, see appendix).
- Run `scripts/merge_translations.py`


### The default language directory

The default directory is of the english language, meaning the `en.lprog` directory.  
To change the default language directory:

- Change in the `scripts/genstrings.sh`  

```
DEFAULT_LANG_DIR=en.lproj
``` 
- Change in the `scripts/localization_configuration.py`

```python
DEFAULT_LANGUAGE_DIRECTORY_NAME = "en.lproj"
``` 


## Appendixes

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


### Convert Localizable.strings from/to proper encoding

**Notice** The Localizable.strings encoding is UTF16, Little Endian, with line ending set as LF.  
The different scripts expect & produce the files in this encoding.  

You can use:
```
iconv -f utf-8 -t utf-16 Localizable.strings > Localizable.new.strings 
```
to convert utf-8 file to the format we use in the scripts.

```
iconv -f utf-16 -t utf-8 Localizable.strings > Localizable.new.strings
```
for the opposite effect. 



