#ifndef PTHREAD_HACK_H
#define PTHREAD_HACK_H
#ifndef PTHREAD_BARRIER_SERIAL_THREAD
#define PTHREAD_BARRIER_SERIAL_THREAD 1234
#endif
#define pthread_barrier_t _hack_pthread_barrier_t
typedef struct {
  struct _pthread_fastlock __ba_lock; /* Lock to guarantee mutual exclusion */
  int __ba_required;                  /* Threads needed for completion */
  int __ba_present;                   /* Threads waiting */
  _pthread_descr __ba_waiting;        /* Queue of waiting threads */
} pthread_barrier_t;
#define pthread_rwlock_t _hack_pthread_rwlock_t
typedef struct
{
  struct _pthread_fastlock __rw_lock; /* Lock to guarantee mutual exclusion */
  int __rw_readers;                   /* Number of readers */
  _pthread_descr __rw_writer;         /* Identity of writer, or NULL if none */
  _pthread_descr __rw_read_waiting;   /* Threads waiting for reading */
  _pthread_descr __rw_write_waiting;  /* Threads waiting for writing */
  int __rw_kind;                      /* Reader/Writer preference selection */
  int __rw_pshared;                   /* Shared between processes or not */
} pthread_rwlock_t;
#endif
