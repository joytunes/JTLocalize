// JTLocalizeUtils.m
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

#import "JTLocalizeUtils.h"

static NSString *gJTDocumentsDirectoryCache = nil;

@implementation JTLocalizeUtils


+ (NSString *)locatePathForFile:(NSString *)fileName {
    NSMutableArray *searchPaths = [NSMutableArray array];
    
    // maybe the file was full path to begin with
    [self addPath:fileName toSearchPaths:searchPaths];
    
    // documents directory
    [self addPath:[self.documentsDirectory stringByAppendingPathComponent:fileName] toSearchPaths:searchPaths];
    
    // app bundle
    NSString *directory = [fileName stringByDeletingLastPathComponent];
    NSString *file = [fileName lastPathComponent];
    [self addPath:[[NSBundle bundleForClass:self] pathForResource:file ofType:nil inDirectory:directory]
    toSearchPaths:searchPaths];
    
    // temp dir
    [self addPath:[NSTemporaryDirectory() stringByAppendingPathComponent:fileName] toSearchPaths:searchPaths];
    
    for (NSString *path in searchPaths) {
        if ([[NSFileManager defaultManager] fileExistsAtPath:path]) {
            return path;
        }
    }
    
    return nil;
}

#pragma mark - Helpers

+ (void)addPath:(NSString *)path toSearchPaths:(NSMutableArray *)paths {
    if (path != nil) {
        [paths addObject:path];
    }
}

+ (NSString *)documentsDirectory {
    if (gJTDocumentsDirectoryCache == nil) {
        NSArray *paths = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
        gJTDocumentsDirectoryCache = (paths.count > 0) ? paths.firstObject : nil;
    }
    return gJTDocumentsDirectoryCache;
}

@end

@implementation NSString (JTLocalizeExtensions)

- (NSString *)stringByLocalizingJTLDirectives {
    NSString *string = self;
    //Intended string : JTL\(['"](.+?)['"],\s*['"](.+?)['"]\)
    NSString *regexString = @"JTL\\(['\"](.+?)['\"],\\s*['\"](.+?)['\"]\\)";
    NSRegularExpression *regex = [NSRegularExpression regularExpressionWithPattern:regexString
                                                                           options:NSRegularExpressionCaseInsensitive
                                                                             error:nil];
    
    NSTextCheckingResult *match = [regex firstMatchInString:string
                                                    options:0
                                                      range:NSMakeRange(0, string.length)];
    while (match != nil) {
        NSRange localizedKeyRange = [match rangeAtIndex:1];
        NSString *localizedKey = [string substringWithRange:localizedKeyRange];
        NSString *localizedString = localizedKey.localizedString;
        string = [string stringByReplacingCharactersInRange:match.range withString:localizedString];
        match = [regex firstMatchInString:string
                                  options:0
                                    range:NSMakeRange(0, string.length)];
    }
    
    return string;
}

- (NSString *)localizedString {
    return JTDynamicLocalizedString(self);
}

@end

@implementation NSAttributedString(JTExtensions)

- (NSAttributedString *)localizedAttributedStringByFragments {
    NSMutableAttributedString *localizedText = self.mutableCopy;
    NSRange range;
    NSUInteger startIndex = localizedText.length - 1;
    while (startIndex > 0) {
        [localizedText attributesAtIndex:startIndex effectiveRange:&range];
        NSString *fragment = [localizedText attributedSubstringFromRange:range].string;
        NSString *localizedFragment = [fragment localizedString];
        [localizedText replaceCharactersInRange:range withString:localizedFragment];
        startIndex = range.location - 1;
    }

    return localizedText;
}

- (BOOL)needsAttributedLocalization {
    if (self.length == 0) {
        return NO;
    }

    NSRange range;
    [self attributesAtIndex:0 effectiveRange:&range];
    return range.length < self.length;
}

@end
