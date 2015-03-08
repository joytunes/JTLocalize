//  DTAttributedLabel+JTLocalizeExtensions.m
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

#import <JTLocalize/JTLocalize.h>
#import "DTAttributedLabel+JTLocalizeExtensions.h"
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
