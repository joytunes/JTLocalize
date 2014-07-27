//
//  DTAttributedLabel+JTLocalizeExtensions.m
//  JTLocalizeExample
//
//  Created by Matan Eilat on 7/24/14.
//  Copyright (c) 2014 JoyTunes. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "DTAttributedLabel+JTLocalizeExtensions.h"
#import "JTLocalizeUtils.h"
#import "UIView+JTLocalizeExtensions.h"

@implementation DTAttributedLabel (JTLocalizeExtensions)

- (NSString *)htmlString {
    return self.attributedString.htmlFragment;
}

- (void)setHtmlString:(NSString *)htmlString {
    htmlString = [htmlString stringByLocalizingJTLDirectives];
    
    self.attributedString =  [[NSAttributedString alloc]
                              initWithHTMLData:[htmlString dataUsingEncoding:NSUTF8StringEncoding]
                              documentAttributes:nil];
    
    CGFloat requiredHeight = [self suggestedFrameSizeToFitEntireStringConstraintedToWidth:self.width].height;
    CGFloat insetSize = (self.height - requiredHeight) / 2;
    self.edgeInsets = UIEdgeInsetsMake(insetSize, 0, insetSize, 0);
}

@end
