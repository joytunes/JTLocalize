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
                                                      [NSDate date].timeIntervalSince1970 * 1000.0]];
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
    [self.currLangLocalizationFileHandle writeData:[line dataUsingEncoding:NSUTF8StringEncoding]];
}

- (void)finishLocalizing {
    [self.currLangLocalizationFileHandle closeFile];
    self.currLangLocalizationFileHandle = nil;
    
    [JTLocalize setLocalizationBundleToPath:self.testBundlePath stringsTableName:nil];
}

- (void)testStringWithoutJTLDirectiveIsNotModified {
    NSString *aString = @"aosidjhawenaljdnaslkdjhas9awhereahrp we4r823 08r";
    NSString *modifiedString = [aString stringByLocalizingJTLDirectives];
    XCTAssertEqualObjects(aString, modifiedString);
}

- (void)testStringWithJTLDirectiveIsProcessed {
    NSString *srcString = @"1 2 JTL(\"3\",\"4\") 5 6 JTL(\"7\",\"8\") 9 10";
    NSString *expectedString = @"1 2 3 5 6 7 9 10";
    NSString *modifiedString = [srcString stringByLocalizingJTLDirectives];
    XCTAssertEqualObjects(modifiedString, expectedString);
}

- (void)testStringWithSingleQuoteJTLDirectiveIsProcessed {
    NSString *srcString = @"1 2 JTL('3','4') 5 6 JTL('7','8') 9 10";
    NSString *expectedString = @"1 2 3 5 6 7 9 10";
    NSString *modifiedString = [srcString stringByLocalizingJTLDirectives];
    XCTAssertEqualObjects(modifiedString, expectedString);
}

- (void)testLocalizeSimpleJTLStringWhenThereIsTranslation {
    [self localizeString:@"Bla" to:@"בלה"];
    [self finishLocalizing];
    
    XCTAssertEqualObjects(@"JTL('Bla', 'BlaBla')".stringByLocalizingJTLDirectives, @"בלה");
}

- (void)testLocalizeMultipleJTLExpressions {
    [self localizeString:@"foo" to:@"shmoo"];
    [self localizeString:@"bar" to:@"shmar"];
    [self finishLocalizing];

    XCTAssertEqualObjects(@"JTL('foo', '')&JTL('bar', '')".stringByLocalizingJTLDirectives, @"shmoo&shmar");
}

- (void)testLocalizeMultilineJTLExpression {
    [self localizeString:@"hey\nhow are you?" to:@"היי\nמה נשמע?"];
    [self finishLocalizing];

    XCTAssertEqualObjects(@"JTL('hey\nhow are you?', '')".stringByLocalizingJTLDirectives, @"היי\nמה נשמע?");
}

@end
