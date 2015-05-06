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

@end

@implementation JTLocalizeTests

- (void)testLocalizeSimpleJTLString {
    XCTAssertEqualObjects(@"JTL('Bla', 'BlaBla')".stringByLocalizingJTLDirectives, @"Bla");
}

@end
