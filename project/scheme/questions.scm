(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))

; Some utility functions that you may find useful to implement.
(define (map proc items)
  (if (null? items) nil (cons (proc (car items)) (map proc (cdr items)))))

(define (cons-all first rests)
  (map (lambda (x) (cons first x)) rests))

(define (zip pairs)
  (list (map (lambda (pair) (car pair)) pairs) (map (lambda (pair) (cadr pair)) pairs))
)


;; Problem 17
;; Returns a list of two-element lists
(define (enumerate s)
  ; BEGIN PROBLEM 17
  (define (helper index lst)
    (if (null? lst) nil
        (cons (list index (car lst)) (helper (+ index 1) (cdr lst)))))
  (helper 0 s)
)
  ; END PROBLEM 17

;; Problem 18
;; List all ways to make change for TOTAL with DENOMS
(define (list-change total denoms)
  ; BEGIN PROBLEM 18
  (cond
    ((<= total 0) '())
    ((null? denoms) '())
    (else 
      (if (= total (car denoms)) (define equalFirst (list (list (car denoms)))) (define equalFirst '()))
      (define restOfUse (list-change (- total (car denoms)) denoms))
      (if (null? restOfUse) (define use '()) (define use (cons-all (car denoms) restOfUse)))
      (define nouse (list-change total (cdr denoms)))
      (append equalFirst use nouse)
    )
  )
)
  ; END PROBLEM 18

;; Problem 19
;; Returns a function that checks if an expression is the special form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (let-to-lambda expr)
  (cond ((atom? expr)
         ; BEGIN PROBLEM 19
         expr
         ; END PROBLEM 19
         )
        ((quoted? expr)
         ; BEGIN PROBLEM 19
         expr
         ; END PROBLEM 19
         )
        ((or (lambda? expr)
             (define? expr))
         (let ((form   (car expr))
               (params (cadr expr))
               (body   (cddr expr)))
           ; BEGIN PROBLEM 19
           (cons form (cons (map let-to-lambda params) (map let-to-lambda body)))
           ; END PROBLEM 19
           ))
        ((let? expr)
         (let ((values (cadr expr))
               (body   (cddr expr)))
           ; BEGIN PROBLEM 19
           (define data (zip values))
           (define params (map let-to-lambda (car data)))
           (define vals (map let-to-lambda (cadr data)))
           (cons (cons 'lambda (cons params (map let-to-lambda body))) vals)
           ; END PROBLEM 19
           ))
        (else
         ; BEGIN PROBLEM 19
          (map let-to-lambda expr)
         ; END PROBLEM 19
         )))
