(define (find s predicate)
  'YOUR-CODE-HERE
  (cond
    ((null? s) #f)
    ((predicate (car s)) (car s))
    (else (find (cdr-stream s) predicate)))
)

(define (scale-stream s k)
  'YOUR-CODE-HERE
  (if
    (null? s) nil
    (cons-stream (* k (car s)) (scale-stream (cdr-stream s) k)))
)

(define (has-cycle s)
  'YOUR-CODE-HERE
  (define (helper slow fast)
    (cond 
      ((or (null? slow) (null? fast) (null? (cdr-stream fast))) #f)
      ((eq? slow fast) #t)
      (else (helper (cdr-stream slow) (cdr-stream (cdr-stream fast)))))
  )
  (if
    (or (null? s) (null? (cdr-stream s))) #f
    (helper s (cdr-stream s)))
)
(define (has-cycle-constant s)
  'YOUR-CODE-HERE
  (define (helper slow fast)
    (cond 
      ((or (null? slow) (null? fast) (null? (cdr-stream fast))) #f)
      ((eq? slow fast) #t)
      (else (helper (cdr-stream slow) (cdr-stream (cdr-stream fast)))))
  )
  (if
    (or (null? s) (null? (cdr-stream s))) #f
    (helper s (cdr-stream s)))
)
