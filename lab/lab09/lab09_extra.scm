;; Extra Scheme Questions ;;

; Q5
(define (square x) (* x x))

(define (pow b n)
  'YOUR-CODE-HERE
  (cond
  ((= n 0) 1)
  ((= (modulo n 2) 0) (square (pow b (quotient n 2))))
  (else (* b (pow b (- n 1)))))
)

; Q6
(define lst
  (list (list 1) 2 (cons 3 4) 5)
)

; Q7
(define (composed f g)
  'YOUR-CODE-HERE
  (lambda (x) (f (g x)))
)

; Q8
(define (remove item lst)
  'YOUR-CODE-HERE
  (cond
    ((null? lst) nil)
    ((= (car lst) item) (remove item (cdr lst)))
    (else (cons (car lst) (remove item (cdr lst)))))
)


;;; Tests
(remove 3 nil)
; expect ()
(remove 3 '(1 3 5))
; expect (1 5)
(remove 5 '(5 3 5 5 1 4 5 4))
; expect (3 1 4 4)

; Q9
(define (max a b) (if (> a b) a b))
(define (min a b) (if (> a b) b a))
(define (gcd a b)
  'YOUR-CODE-HERE
  (cond
    ((= (min a b) 0) (max a b))
    ((= (modulo (min a b) (max a b)) 0) (min a b))
    (else (gcd (min a b) (modulo (max a b) (min a b)))))
)

;;; Tests
(gcd 24 60)
; expect 12
(gcd 1071 462)
; expect 21

; Q10
(define (no-repeats s)
  'YOUR-CODE-HERE
  (define temp 0)
  (define (f? val) (not (= temp val)))
  (cond
    ((null? s) nil)
    (else (define temp (car s)) (cons temp (no-repeats (filter f? (cdr s))))))
)

; Q11
(define (substitute s old new)
  'YOUR-CODE-HERE
  (cond
    ((null? s) nil)
    ((pair? (car s)) (cons (substitute (car s) old new) (substitute (cdr s) old new)))
    ((eq? (car s) old) (cons new (substitute (cdr s) old new)))
    (else (cons (car s) (substitute (cdr s) old new)))
  )
)

; Q12
(define (sub-all s olds news)
  'YOUR-CODE-HERE
  (define (getitem lst pos)
    (if (= pos 0) (car lst) (getitem (cdr lst) (- pos 1)))
  )
  (define (getpos lst val count)
    (cond
      ((null? lst) -1)
      ((eq? (car lst) val) count)
      (else (getpos (cdr lst) val (+ count 1)))
    )
  )
  (cond
    ((null? s) nil)
    ((pair? (car s)) (cons (sub-all (car s) olds news) (sub-all (cdr s) olds news)))
    ((not (= (getpos olds (car s) 0) -1)) (cons (getitem news (getpos olds (car s) 0)) (sub-all (cdr s) olds news)))
    (else (cons (car s) (sub-all (cdr s) olds news)))
  )
)