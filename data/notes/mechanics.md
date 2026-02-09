# Mechanics – IIT-JEE Notes

## 1. Kinematics

### Key Concepts
- **Displacement** is a vector; **distance** is a scalar.
- Equations of motion (constant acceleration):
  - v = u + at
  - s = ut + ½at²
  - v² = u² + 2as
- **Projectile Motion**: Treat horizontal and vertical components independently.
  - Range R = u²sin(2θ)/g, max at θ = 45°
  - Time of flight T = 2u sinθ / g
  - Max height H = u²sin²θ / (2g)
- **Relative Motion**: v_AB = v_A − v_B. Use for river-boat, rain-man problems.

### Common JEE Traps
- Forgetting that acceleration due to gravity is negative when upward is positive.
- Mixing up average speed vs average velocity.
- In projectile motion, horizontal acceleration = 0 (ignore air resistance).

### Important Problems
1. A ball is thrown at 30° with speed 20 m/s. Find the range and max height.
2. Two cars start from rest with accelerations 2 m/s² and 4 m/s². When does the second overtake the first if it starts 5 s late?

---

## 2. Newton's Laws of Motion

### Key Concepts
- **First Law**: A body remains in its state unless acted upon by a net external force.
- **Second Law**: F = ma (vector form: **F** = m**a**)
- **Third Law**: Every action has an equal and opposite reaction.
- **Free Body Diagram (FBD)**: Always draw FBDs before solving. Identify all forces: weight, normal, tension, friction, applied forces.
- **Friction**:
  - Static friction: f_s ≤ μ_s N
  - Kinetic friction: f_k = μ_k N (μ_k < μ_s)
- **Pseudo forces** in non-inertial frames: F_pseudo = −ma_frame

### Common JEE Traps
- Not accounting for all forces in FBD.
- Constraint equations: when pulleys or strings connect bodies, use constraints (e.g., if one end moves x, the other end moves 2x for a movable pulley).
- Circular motion: centripetal acceleration = v²/r directed toward center.

### Important Formulas
- For connected blocks on a surface: a = (F − f) / (m₁ + m₂)
- Banked turn without friction: tan θ = v²/(rg)

---

## 3. Work, Energy & Power

### Key Concepts
- **Work**: W = **F** · **d** = Fd cos θ
- **Kinetic Energy**: KE = ½mv²
- **Work-Energy Theorem**: W_net = ΔKE
- **Potential Energy**:
  - Gravitational: U = mgh
  - Spring: U = ½kx²
- **Conservation of Energy**: KE₁ + PE₁ = KE₂ + PE₂ (if no non-conservative work)
- **Power**: P = dW/dt = **F** · **v**

### Common JEE Traps
- Work done by friction is negative and path-dependent.
- Spring PE is measured from natural length.
- In vertical circular motion, minimum speed at top = √(gr).

---

## 4. Rotational Mechanics

### Key Concepts
- **Torque**: τ = r × F, magnitude = rF sinθ
- **Moment of Inertia**: I = Σmᵢrᵢ² (or ∫r² dm for continuous bodies)
  - Rod (center): ML²/12, Rod (end): ML²/3
  - Disc (center): MR²/2, Ring: MR²
  - Sphere (solid): 2MR²/5, Sphere (hollow): 2MR²/3
- **Parallel axis theorem**: I = I_cm + Md²
- **Perpendicular axis theorem** (2D bodies): I_z = I_x + I_y
- **Angular momentum**: L = Iω; τ = dL/dt
- **Rolling without slipping**: v_cm = Rω; a_cm = Rα

### Important Formulas
- KE of rolling body = ½mv² + ½Iω² = ½mv²(1 + k²/R²)
- For pure rolling down an incline: a = g sinθ / (1 + I/(mR²))

---

## 5. Gravitation

### Key Concepts
- **Newton's Law of Gravitation**: F = GMm/r²
- **Gravitational field**: g = GM/r²
- Inside a solid sphere (r < R): g = GMr/R³
- **Gravitational PE**: U = −GMm/r
- **Orbital velocity**: v_o = √(GM/r)
- **Escape velocity**: v_e = √(2GM/R) = √(2gR)
- **Kepler's Laws**:
  1. Elliptical orbits
  2. Equal areas in equal times (conservation of L)
  3. T² ∝ a³

---

## 6. Simple Harmonic Motion

### Key Concepts
- **SHM**: a = −ω²x; x(t) = A sin(ωt + φ)
- **Time period**:
  - Spring-mass: T = 2π√(m/k)
  - Simple pendulum: T = 2π√(l/g)
- **Energy**: E = ½kA² = ½mω²A² (constant)
  - KE = ½mω²(A²−x²), PE = ½mω²x²
- **Superposition of SHMs**: Use phasor method or trigonometric identities.

### Common JEE Traps
- Phase difference matters in superposition.
- For physical pendulum: T = 2π√(I/(mgl))
- Damped oscillations and resonance (conceptual).

