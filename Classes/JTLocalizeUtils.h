// JTLocalizeUtils.h
//
// Copyright (c) 2015 JoyTunes (http://joytunes.com)
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
// THE SOFTWARE.

#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>

extern NSString *const kJTDefaultLocalizationBundleName;
extern NSString *const kJTDefaultStringsTableName;


#define JTLocalizedString(aKey, aComment) ([JTLocalize localizedStringForKey:(aKey) comment:(aComment)])

// For localizing variables. Act the same as JTLocalizedString, but scripts won't complain about it.
#define JTDynamicLocalizedString(key) (JTLocalizedString((key), @""))

@interface JTLocalize : NSObject

// Calling this will allow JTLocalize to search for strings in a new bundle path
// This is useful if you want your app to download this bundle from a remote server:
// will allow you to dynamically change all internationalized strings in your app.
// (notice that NSBundles are cached, so call this only once you're finished downloading)
// Giving nil in each parameters will cause the defaults to be restored.
+ (void)setLocalizationBundleToPath:(NSString *)bundlePath stringsTableName:(NSString *)tableName;

// Optionally provide a preferredLocale argument to setLocalizationBundleToPath,
// this would point to the specific <preferredLocale.lproj> sub-path in the bundle
// and the strings file there would be used regardless of locale setting of the device
+ (void)setLocalizationBundleToPath:(NSString *)bundlePath stringsTableName:(NSString *)tableName preferredLocale:(NSString *)preferredLocale;

// Returns the effective locale identifier used from the bundle
+ (NSString *)effectiveLocale;

// Returns true if the effective locale is right to left. Otherwise, returns false.
+ (BOOL)isRightToLeft;

// Will search the string in the pre-set bundle path.
// If not set otherwise: will search kJTDefaultLocalizationBundleName in the app bundle,
// and will use kJTDefaultStringsTableName
+ (NSString *)localizedStringForKey:(NSString *)key comment:(NSString *)comment;

@end

@interface NSString (JTLocalizeExtensions)

- (NSString *)stringByLocalizingJTLDirectives;

- (NSString *)localizedString;

// Check if the string matches the JTL Directive by looking for the localization regular expression.
// In case there is a match, the method will return the match as NSTextCheckingResult object.
// Otherwise, will return nil.
- (NSTextCheckingResult *)matchForJTLDirective;

@end

@interface NSAttributedString(JTLocalizeExtensions)

// Divide the string into fragments by asking for the effective range of an attribute set
// For each such range, extract the string, localize and inject back inside.
- (NSAttributedString *)localizedAttributedStringByFragments;

- (BOOL)needsAttributedLocalization;

@end

@interface UIView(JTLocalizeExtensions)

- (void)localizeTextPropertyNamed:(NSString *)propertyName;

@end
