//
//  JTButton.h
//  JTLocalizeExample
//
//  Created by Matan Eilat on 7/24/14.
//  Copyright (c) 2014 JoyTunes. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface JTButton : UIButton

@property (nonatomic, assign) BOOL customizeStates;

//Use like numberOfLines in UILabel
@property (nonatomic, assign) int numberOfLines;

@end
