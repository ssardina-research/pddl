(define (domain blocks-world-domain)
  (:requirements :strips :equality :conditional-effects :non-deterministic)

  (:constants Table)

  (:predicates (on ?x ?y)
	       (clear ?x)
	       (block ?b)
	       )

  ;; Define step for placing one block on another.
  (:action puton
     :parameters (?x ?y ?z)
     :precondition (and (on ?x ?z) (clear ?x) (clear ?y)
             (not (= ?y ?z)) (not (= ?x ?z))
             (not (= ?x ?y)) (not (= ?x Table)))
     :effect
            (oneof
            (and (on ?x ?y) (not (on ?x ?z))
            (when (not (= ?z Table)) (clear ?z))
            (when (not (= ?y Table)) (not (clear ?y)))
            )
            (and (on ?x Table)
            (when (not (= ?z Table)) (and (not (on ?x ?z)) (clear ?z)))
            (when (not (= ?y Table)) (not (clear ?y)))
            )
            )
       )
	)

(define (problem sussman-anomaly)       ; graphplan 3 steps
    (:domain blocks-world-domain)
  (:objects A B C)
  (:init (block A) (block B) (block C) (block Table)
	 (on C A) (on A Table) (on B Table)
	 (clear C) (clear B) (clear Table))
  (:goal (on B A))
)
