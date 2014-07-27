//
//  JTLocalizeUtils.h
//  JTLocalizeExample
//
//  Created by Matan Eilat on 7/24/14.
//  Copyright (c) 2014 JoyTunes. All rights reserved.
//

#import <Foundation/Foundation.h>

#define kJTLocalizationBundle (@"JTLocalizable.bundle")
#define kJTStringsTableName (@"Localizable")

#define JTLocalizedString(key, comment) (NSLocalizedStringFromTableInBundle((key), kJTStringsTableName, [NSBundle bundleWithPath:[JTLocalizeUtils locatePathForFile:kJTLocalizationBundle]], (comment)) ?: key)

// For localizing variables. Act the same as JTLocalizedString, but scripts won't complain about it.
#define JTDynamicLocalizedString(key) (JTLocalizedString((key), @""))

@interface JTLocalizeUtils : NSObject

+ (NSString *)locatePathForFile:(NSString *)fileName;

@end

@interface NSString (JTLocalizeExtensions)

- (NSString *)stringByLocalizingJTLDirectives;

@end
