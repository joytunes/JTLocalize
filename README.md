![JTLocalize](https://github.com/joytunes/JTLocalize/blob/master/JTLocalize/logo.png)
==========

### Abstract

Apple provides nice tools for internationalization and localization (See [official documentation](https://developer.apple.com/internationalization/)).
However, we had several pains that weren't answered out of the box easily:
- **Multiple .strings files to maintain**: `genstrings` will extract NSLocalizedString strings from code, but for each IB document you internationalize - you need to have a separate .strings file, which causes painful maintenance of strings for localization. Also - this way if you already localized a common expression that appears in several files, you'll need to remember to update it for each file separately.
- **Localizing a new version is very painful**: When you change a view in IB, its .strings file can immediately become invalid and it is very hard to make use of the existing localizations of previous versions. This is also true for the .strings that are extracted by `genstrings`.
- **NSLocalizedString assumes strings are in main bundle**: If you want to use another localization bundle path (e.g. some path of a file you download from your server in runtime), you need to use other more complex macros.

**JTLocalize** was written to solve these pains:
- **Unified .strings file**: Collection of multiple localizable strings from multiple types of resources throughout the project. No need for separate strings file per storyboard/xib - Only one file to maintain without duplicate strings.
- **Continuous translation intergration simplified**: When the app changes, you don't need to localize everything again. `jtlocalize` command-line tools will make it easy to just send the diff for translation and merge the translated diff back.
- **Configurable location of localization bundle**: This allows you to easily decide to use the main bundle as default, and move to another path once you downloaded it from server. As a side effect of this, you can easily use JTLocalize to change all the English versions of your strings from server.


## How to internationalize (Preparing your project's strings for the unified .strings file)

Internationalization is done using custom objective-c classes and simple marking mechanisms.

### Adding to your project

JTLocalize can be added to an Xcode project using [CocoaPods](http://cocoapods.org):

```ruby
pod "JTLocalize"
```

### Internationalizing UI Elements

Internationalization of UI elements works for both xibs and storyboard files.

In order to internationalize UI element (`UIBotton`,`UILabel`,`UITextField`, ...):
- Use the corresponding class in the JTLocalize framework (`JTButton`, `JTLabel`, `JTTextField`, ...) as the <b>Custom Class</b> of the UI element.
These classes use the proper localized string when setting the text.

- In interface Builder's Document Outline, set the element's "userLabel" (Document->Label) to a string with the `JTL_` prefix.
This prefix is respected by our localization command-line tool for string extraction.
The rest of the string in the userLabel (after the `JTL_` prefix) will be used as the comment of the localization entry in the Localizable.strings files.

![The JTL_ prefix](https://github.com/joytunes/JTLocalize/blob/master/JTLocalize_storyboard.png)


#### Internationalizing DTCoreText attributed labels
To internationalize `DTCoreText` elements (`DTAttributedLabel`) see the illustration in the example project (DTAttributedLabel+JTLocalizeExtensions, JTAttributedLabelWithLink).
The reason this is only in the example project is to avoid `DTCoreText` dependency in the Pod.

If you want to use them (and internationalize them), add a **keypath named htmlString** with an html string value.
In this html string value, simply put `JTL("Key", "Comment")` wherever you would a localized string value.

### Internationalizing strings in code

To internationalize strings in the code, simply use the JTLocalizedString() macro (exactly as you would use NSLocalizedString() normally, but with a different macro):
```objective-c
NSString *localizedString = JTLocalizedString("Some string", "The Strings context for translation")
```

#### Swift

Swift doesn't support C-macros. We currently didn't insert any Swift functions into the Pod itself, because CocoaPods' Swift support is still in beta (as of writing these lines).

Instead, we attached a POC to our example project to show you how you can easily use `JTLocalize` in your Swift projects. 
See [JTSwiftPOC.swift](https://github.com/joytunes/JTLocalize/blob/master/example/JTLocalizeExample/JTSwiftPOC.swift)

## How to localize

The JTLocalize framework provides the `jtlocalize` command line tool that integrate with the internationalization mechanisms, and simplify the localization flow.

### Installation

This application requires:

* [Python 2.x](https://www.python.org/download/)

Install with `pip install jtlocalize`, or download the latest release version:

* Release: [https://pypi.python.org/pypi/jtlocalize](https://pypi.python.org/pypi/jtlocalize) [![Version](http://img.shields.io/pypi/v/jtlocalize.svg?style=flat)](https://pypi.python.org/pypi/jtlocalize)

### The standard localization flow

Usually we will use the `generate`, `prepare_diff` and `merge` sub-operations of the `jtlocalize` command-line tool, in the following manner:
- Make sure your `JTLocalizable.bundle` is ready with directories for all the languages you need 
(see appendix for more info)
- Run `jtlocalize generate /path/to/project /path/to/JTLocalizable.bundle`
- Run `jtlocalize prepare_diff /path/to/JTLocalizable.bundle`
- Translate the `Localizable.strings.pending` files in the different languages directories  
(convert encoding if needed, see appendix).
- Save the translated file in the proper language directory under `Localizable.strings.translated`  
(convert encoding if needed, see appendix).
- Run `jtlocalize merge /path/to/JTLocalizable.bundle`


#### mock_translate

Another useful sub-operation that can help you make sure you didn't forget to internationalize any strings in your app.

Example Usage:
```
jtlocalize mock_translate --preset chicken /path/to/Localizable.strings
```
Will localize the given file so that all translations are "Chicken".

#### word_count

Often we need to send a pending strings file to a 3rd party translation service, which charge us by a word count.
To get an accurate word count of the words that actually needs to be translated, you can run: 
`jtlocalize word_count /path/to/Localizable.strings.pending`

#### More operations and flags

`jtlocalize` supports many flags and features for configuring your localization flow.
You can run `jtlocalize --help` or `jtlocalize OPERATION --help` to gen information about all of them.


## Appendices

### JTLocalizable.bundle - The localization bundle

The localize bundle is the directory containing the strings files for the different languages the app is localized to.

For example:

JTLocalizable.bundle  
|&nbsp;&nbsp;&nbsp;+-- en.lproj  
|&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;+-- Localizable.strings  
|&nbsp;&nbsp;&nbsp;+-- ru.lproj  
|&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;+-- Localizable.strings  

The `jtlocalize` command_line tools assume en.lproj is the default language directory (will be configurable in future).
Whenever you need to add a new language, just make sure you add an empty LANGUAGE_CODE.lproj directory to the bundle before running `prepare_diff`.

### Convert Localizable.strings from/to proper encoding

**Notice**: The Localizable.strings encoding is UTF16, Little Endian, with line ending set as LF.  
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
