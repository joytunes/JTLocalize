//
//  JTLabel.h
//  JTLocalizeExample
//
//  Created by Matan Eilat on 7/23/14.
//  Copyright (c) 2014 JoyTunes. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface JTLabel : UILabel


@property (nonatomic, strong) UIColor* strokeColor;
@property (nonatomic) CGFloat strokeWidth;
@property (nonatomic) BOOL forceNonAttrStringInIOS6;

@end
