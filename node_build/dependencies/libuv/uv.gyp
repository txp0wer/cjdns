{
  'variables': {
    'uv_use_dtrace%': 'false',
    # uv_parent_path is the relative path to libuv in the parent project
    # this is only relevant when dtrace is enabled and libuv is a child project
    # as it's necessary to correctly locate the object files for post
    # processing.
    # XXX gyp is quite sensitive about paths with double / they don't normalize
    'uv_parent_path': '/',
  },

  'target_defaults': {
    'conditions': [
      ['OS != "win"', {
        'defines': [
          '_LARGEFILE_SOURCE',
          '_FILE_OFFSET_BITS=64',
        ],
        'conditions': [
          ['OS=="solaris"', {
            'cflags': [ '-pthreads' ],
          }],
          ['OS not in "solaris android"', {
            'cflags': [ '-pthread' ],
          }],
        ],
      }],
    ],
  },

  'targets': [
    {
      'target_name': 'libuv',
      'type': '<(library)',
      'include_dirs': [
        'include',
        'src/',
      ],
      'direct_dependent_settings': {
        'include_dirs': [ 'include' ],
        'conditions': [
          ['OS != "win"', {
            'defines': [
              '_LARGEFILE_SOURCE',
              '_FILE_OFFSET_BITS=64',
            ],
          }],
          ['OS == "mac"', {
            'defines': [ '_DARWIN_USE_64_BIT_INODE=1' ],
          }],
          ['OS == "linux"', {
            'defines': [ '_POSIX_C_SOURCE=200112' ],
          }],
        ],
      },
      'defines': [
        'HAVE_CONFIG_H'
      ],
      'sources': [
        'common.gypi',
        'include/uv.h',
        'include/tree.h',
        'include/uv-errno.h',
        'src/fs-poll.c',
        'src/inet.c',
        'src/queue.h',
        'src/uv-common.c',
        'src/uv-common.h',
        'src/version.c'
      ],
      'conditions': [
        [ 'OS=="win"', {
          'defines': [
            '_WIN32_WINNT=0x0600',
            '_GNU_SOURCE',
          ],
          'sources': [
            'include/uv-win.h',
            'src/win/async.c',
            'src/win/atomicops-inl.h',
            'src/win/core.c',
            'src/win/dl.c',
            'src/win/error.c',
            'src/win/fs.c',
            'src/win/fs-event.c',
            'src/win/getaddrinfo.c',
            'src/win/handle.c',
            'src/win/handle-inl.h',
            'src/win/internal.h',
            'src/win/iocp.c',
            'src/win/loop-watcher.c',
            'src/win/pipe.c',
            'src/win/thread.c',
            'src/win/poll.c',
            'src/win/process.c',
            'src/win/process-stdio.c',
            'src/win/req.c',
            'src/win/req-inl.h',
            'src/win/signal.c',
            'src/win/stream.c',
            'src/win/stream-inl.h',
            'src/win/tcp.c',
            'src/win/tty.c',
            'src/win/threadpool.c',
            'src/win/timer.c',
            'src/win/udp.c',
            'src/win/util.c',
            'src/win/winapi.c',
            'src/win/winapi.h',
            'src/win/winsock.c',
            'src/win/winsock.h',
          ],
          'link_settings': {
            'libraries': [
              '-ladvapi32',
              '-liphlpapi',
              '-lpsapi',
              '-lshell32',
              '-lws2_32'
            ],
          },
        }, { # Not Windows i.e. POSIX
          'cflags': [
            '-g',
            '--std=gnu89',
            '-pedantic',
            '-Wall',
            '-Wextra',
            '-Wno-unused-parameter',
          ],
          'sources': [
            'include/uv-unix.h',
            'include/uv-linux.h',
            'include/uv-sunos.h',
            'include/uv-darwin.h',
            'include/uv-bsd.h',
            'src/unix/async.c',
            'src/unix/atomic-ops.h',
            'src/unix/core.c',
            'src/unix/dl.c',
            'src/unix/fs.c',
            'src/unix/getaddrinfo.c',
            'src/unix/internal.h',
            'src/unix/loop.c',
            'src/unix/loop-watcher.c',
            'src/unix/pipe.c',
            'src/unix/poll.c',
            'src/unix/process.c',
            'src/unix/signal.c',
            'src/unix/spinlock.h',
            'src/unix/stream.c',
            'src/unix/tcp.c',
            'src/unix/thread.c',
            'src/unix/threadpool.c',
            'src/unix/timer.c',
            'src/unix/tty.c',
            'src/unix/udp.c',
          ],
          'link_settings': {
            'libraries': [ '-lm' ],
            'conditions': [
              ['OS=="solaris"', {
                'ldflags': [ '-pthreads' ],
              }],
              ['OS != "solaris" and OS != "android"', {
                'ldflags': [ '-pthread' ],
              }],
            ],
          },
          'conditions': [
            ['library=="shared_library"', {
              'cflags': [ ],
            }],
            ['library=="shared_library" and OS!="mac"', {
              'link_settings': {
                # Must correspond with UV_VERSION_MAJOR and UV_VERSION_MINOR
                # in src/version.c
                'libraries': [ '-Wl,-soname,libuv.so.0.11' ],
              },
            }],
          ],
        }],
        [ 'OS in "linux mac android"', {
          'sources': [ 'src/unix/proctitle.c' ],
        }],
        [ 'OS=="mac"', {
          'sources': [
            'src/unix/darwin.c',
            'src/unix/fsevents.c',
            'src/unix/darwin-proctitle.c',
          ],
          'defines': [
            '_DARWIN_USE_64_BIT_INODE=1',
          ]
        }],
        [ 'OS!="mac"', {
          # Enable on all platforms except OS X. The antique gcc/clang that
          # ships with Xcode emits waaaay too many false positives.
          'cflags': [ '-Wstrict-aliasing' ],
        }],
        [ 'OS=="linux"', {
          'sources': [
            'src/unix/linux-core.c',
            'src/unix/linux-inotify.c',
            'src/unix/linux-syscalls.c',
            'src/unix/linux-syscalls.h',
          ],
          'link_settings': {
            'libraries': [ '-ldl', '-lrt' ],
          },
        }],
        [ 'OS=="android"', {
          'sources': [
            'src/unix/linux-core.c',
            'src/unix/linux-inotify.c',
            'src/unix/linux-syscalls.c',
            'src/unix/linux-syscalls.h',
            'src/unix/pthread-fixes.c',
          ],
          'link_settings': {
            'libraries': [ '-ldl' ],
          },
        }],
        [ 'OS=="solaris"', {
          'sources': [ 'src/unix/sunos.c' ],
          'defines': [
            '__EXTENSIONS__',
            '_XOPEN_SOURCE=500',
          ],
          'link_settings': {
            'libraries': [
              '-lkstat',
              '-lnsl',
              '-lsendfile',
              '-lsocket',
            ],
          },
        }],
        [ 'OS=="aix"', {
          'include_dirs': [ 'src/ares/config_aix' ],
          'sources': [ 'src/unix/aix.c' ],
          'defines': [
            '_ALL_SOURCE',
            '_XOPEN_SOURCE=500',
          ],
          'link_settings': {
            'libraries': [
              '-lperfstat',
            ],
          },
        }],
        [ 'OS=="freebsd" or OS=="dragonflybsd"', {
          'sources': [ 'src/unix/freebsd.c' ],
        }],
        [ 'OS=="openbsd"', {
          'sources': [ 'src/unix/openbsd.c' ],
        }],
        [ 'OS=="netbsd"', {
          'sources': [ 'src/unix/netbsd.c' ],
        }],
        [ 'OS in "freebsd dragonflybsd openbsd netbsd".split()', {
          'link_settings': {
            'libraries': [ '-lkvm' ],
          },
        }],
        [ 'OS in "mac freebsd dragonflybsd openbsd netbsd".split()', {
          'sources': [ 'src/unix/kqueue.c' ],
        }],
        ['library=="shared_library"', {
          'defines': [ 'BUILDING_UV_SHARED=1' ]
        }],
        # FIXME(bnoordhuis or tjfontaine) Unify this, it's extremely ugly.
        ['uv_use_dtrace=="true"', {
          'defines': [ 'HAVE_DTRACE=1' ],
          'dependencies': [ 'uv_dtrace_header' ],
          'include_dirs': [ '<(SHARED_INTERMEDIATE_DIR)' ],
          'conditions': [
            [ 'OS not in "mac linux"', {
              'sources': [ 'src/unix/dtrace.c' ],
            }],
            [ 'OS=="linux"', {
              'sources': [ '<(SHARED_INTERMEDIATE_DIR)/dtrace.o' ]
            }],
          ],
        }],
      ]
    },
    {
      'target_name': 'uv_dtrace_header',
      'type': 'none',
      'conditions': [
        [ 'uv_use_dtrace=="true"', {
          'actions': [
            {
              'action_name': 'uv_dtrace_header',
              'inputs': [ 'src/unix/uv-dtrace.d' ],
              'outputs': [ '<(SHARED_INTERMEDIATE_DIR)/uv-dtrace.h' ],
              'action': [ 'dtrace', '-h', '-xnolibs', '-s', '<@(_inputs)',
                '-o', '<@(_outputs)' ],
            },
          ],
        }],
      ],
    },

    # FIXME(bnoordhuis or tjfontaine) Unify this, it's extremely ugly.
    {
      'target_name': 'uv_dtrace_provider',
      'type': 'none',
      'conditions': [
        [ 'uv_use_dtrace=="true" and OS not in "mac linux"', {
          'actions': [
            {
              'action_name': 'uv_dtrace_o',
              'inputs': [
                'src/unix/uv-dtrace.d',
                '<(PRODUCT_DIR)/obj.target/libuv<(uv_parent_path)src/unix/core.o',
              ],
              'outputs': [
                '<(PRODUCT_DIR)/obj.target/libuv<(uv_parent_path)src/unix/dtrace.o',
              ],
              'action': [ 'dtrace', '-G', '-xnolibs', '-s', '<@(_inputs)',
                '-o', '<@(_outputs)' ]
            }
          ]
        }],
        [ 'uv_use_dtrace=="true" and OS=="linux"', {
          'actions': [
            {
              'action_name': 'uv_dtrace_o',
              'inputs': [ 'src/unix/uv-dtrace.d' ],
              'outputs': [ '<(SHARED_INTERMEDIATE_DIR)/dtrace.o' ],
              'action': [
                'dtrace', '-C', '-G', '-s', '<@(_inputs)', '-o', '<@(_outputs)'
              ],
            }
          ]
        }],
      ]
    },

  ]
}
