//
//  JTLocalizeUtils.m
//  JTLocalizeExample
//
//  Created by Matan Eilat on 7/24/14.
//  Copyright (c) 2014 JoyTunes. All rights reserved.
//

#import "JTLocalizeUtils.h"

static NSString *gJTDocumentsDirectoryCache = nil;

@implementation JTLocalizeUtils


+ (NSString *)locatePathForFile:(NSString *)fileName {
    NSMutableArray *searchPaths = [NSMutableArray array];
    
    // maybe the file was full path to begin with
    [self addPath:fileName toSearchPaths:searchPaths];
    
    // documents directory
    [self addPath:self.documentsDirectory toSearchPaths:searchPaths];
    
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
