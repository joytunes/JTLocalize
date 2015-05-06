//
//  JTLocalizeTestsTests.m
//  JTLocalizeTestsTests
//
//  Created by Yoni Tsafir on 5/6/15.
//  Copyright (c) 2015 JoyTunes. All rights reserved.
//

#import <XCTest/XCTest.h>
#import <JTLocalize/JTLocalize.h>

@interface JTLocalizeTests : XCTestCase

@property (nonatomic) NSString *testBundlePath;
@property (nonatomic) NSFileHandle *currLangLocalizationFileHandle;

@end

@implementation JTLocalizeTests

- (void)setUp {
    [super setUp];
    
    self.testBundlePath = [NSTemporaryDirectory() stringByAppendingPathComponent:
                           [NSString stringWithFormat:@"JTLocalizeTestBundle%.0f.bundle",
                                                      [NSDate date].timeIntervalSince1970]];
    NSString *currLangDir = [self.testBundlePath stringByAppendingPathComponent:@"en.lproj"];
    NSString *currLangLocalizationFileName = [[currLangDir stringByAppendingPathComponent:kJTDefaultStringsTableName]
                                              stringByAppendingPathExtension:@"strings"];
    
    [[NSFileManager defaultManager] createDirectoryAtPath:currLangDir withIntermediateDirectories:YES
                                               attributes:nil error:nil];
    
    [[NSFileManager defaultManager] createFileAtPath:currLangLocalizationFileName contents:nil attributes:nil];
    self.currLangLocalizationFileHandle = [NSFileHandle fileHandleForWritingAtPath:currLangLocalizationFileName];
}

- (void)tearDown {
    [self.currLangLocalizationFileHandle closeFile];
    [JTLocalize setLocalizationBundleToPath:nil stringsTableName:nil];
    [[NSFileManager defaultManager] removeItemAtPath:self.testBundlePath error:nil];
    
    [super tearDown];
}

- (void)localizeString:(NSString *)key to:(NSString *)value {
    NSString *line = [NSString stringWithFormat:@"\"%@\" = \"%@\";\n", key, value];
    [self.currLangLocalizationFileHandle writeData:[line dataUsingEncoding:NSUTF16StringEncoding]];
}

- (void)finishLocalizing {
    [self.currLangLocalizationFileHandle closeFile];
    self.currLangLocalizationFileHandle = nil;
    
    [JTLocalize setLocalizationBundleToPath:self.testBundlePath stringsTableName:nil];
}

- (void)testLocalizeSimpleJTLStringNoTranslation {
    XCTAssertEqualObjects(@"JTL('Bla', 'BlaBla')".stringByLocalizingJTLDirectives, @"Bla");
}

- (void)testLocalizeSimpleJTLStringWhenThereIsTranslation {
    [self localizeString:@"Bla" to:@"בלה"];
    [self finishLocalizing];
    
    XCTAssertEqualObjects(@"JTL('Bla', 'BlaBla')".stringByLocalizingJTLDirectives, @"בלה");
}

@end
