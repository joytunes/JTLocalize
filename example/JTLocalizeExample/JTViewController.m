//
//  JTViewController.m
//  JTLocalizeExample
//
//  Created by Matan Eilat on 7/23/14.
//  Copyright (c) 2014 JoyTunes. All rights reserved.
//

#import "JTViewController.h"
#import "JTLocalizeExample-Swift.h"
#import <JTLocalize/JTLocalize.h>

@interface JTViewController () <DTLabelLinkDelegate>

@end

@implementation JTViewController

- (void)viewDidLoad
{
    [super viewDidLoad];
	self.anAttributedLabelWithLink.linkDelegate = self;
    [[[JTSwiftPOC alloc] init] foo];
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (void)label:(id)sender clickedOnUrl:(NSURL *)url {
    UIAlertView *alert = [[UIAlertView alloc] initWithTitle:JTLocalizedString(@"Clicked link", @"A title")
                                                    message:JTLocalizedString(@"Clicked link", @"A message")
                                                   delegate:nil
                                          cancelButtonTitle:@"OK"
                                          otherButtonTitles:nil];
    [alert show];
}

@end
