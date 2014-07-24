//
//  JTViewController.m
//  JTLocalizeExample
//
//  Created by Matan Eilat on 7/23/14.
//  Copyright (c) 2014 JoyTunes. All rights reserved.
//

#import "JTViewController.h"

@interface JTViewController () <DTLabelLinkDelegate>

@end

@implementation JTViewController

- (void)viewDidLoad
{
    [super viewDidLoad];
	self.anAttributedLabelWithLink.linkDelegate = self;
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (void)label:(id)sender clickedOnUrl:(NSURL *)url {
    UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Clicked link"
                                                    message:@"You clicked the link!"
                                                   delegate:nil
                                          cancelButtonTitle:@"OK"
                                          otherButtonTitles:nil];
    [alert show];
}

@end
