# Calculus – IIT-JEE Notes

## 1. Functions

### Key Concepts
- **Domain & Range**: Find domain by identifying restrictions (denominator ≠ 0, √ ≥ 0, log argument > 0).
- **Types of functions**:
  - One-one (injective): f(a) = f(b) ⟹ a = b
  - Onto (surjective): Range = Codomain
  - Bijective: Both one-one and onto (invertible)
- **Composition**: (f∘g)(x) = f(g(x)); domain = {x ∈ Dom(g) : g(x) ∈ Dom(f)}
- **Inverse**: f⁻¹ exists iff f is bijective. Reflect graph about y = x.
- **Even function**: f(−x) = f(x); **Odd function**: f(−x) = −f(x)
- **Periodic function**: f(x + T) = f(x); T is the period.

### Common JEE Traps
- |sin x| has period π, not 2π.
- f(x) = x² is not one-one on ℝ, but is one-one on [0, ∞).

---

## 2. Limits & Continuity

### Key Concepts
- **Definition**: lim(x→a) f(x) = L means ∀ε > 0, ∃δ > 0 s.t. |x−a| < δ ⟹ |f(x)−L| < ε
- **Standard limits**:
  - lim(x→0) sin(x)/x = 1
  - lim(x→0) (eˣ − 1)/x = 1
  - lim(x→0) (aˣ − 1)/x = ln(a)
  - lim(x→0) (1 + x)^(1/x) = e
  - lim(x→∞) (1 + 1/n)^n = e
- **L'Hôpital's Rule**: For 0/0 or ∞/∞ forms: lim f/g = lim f'/g'
- **Squeeze Theorem**: If g(x) ≤ f(x) ≤ h(x) and lim g = lim h = L, then lim f = L.

### Continuity
- f is continuous at x = a if: lim(x→a) f(x) = f(a)
- **Types of discontinuity**:
  - Removable: limit exists but ≠ f(a)
  - Jump: left limit ≠ right limit
  - Infinite: limit is ±∞
- **Intermediate Value Theorem (IVT)**: If f is continuous on [a,b] and f(a) < k < f(b), then ∃c ∈ (a,b) with f(c) = k.

---

## 3. Differentiation

### Key Concepts
- **First Principles**: f'(x) = lim(h→0) [f(x+h) − f(x)] / h
- **Rules**: (fg)' = f'g + fg'; (f/g)' = (f'g − fg')/g²
- **Chain Rule**: d/dx[f(g(x))] = f'(g(x)) · g'(x)
- **Standard derivatives**:
  - d/dx(xⁿ) = nxⁿ⁻¹
  - d/dx(eˣ) = eˣ; d/dx(aˣ) = aˣ ln a
  - d/dx(ln x) = 1/x
  - d/dx(sin x) = cos x; d/dx(cos x) = −sin x
  - d/dx(tan x) = sec²x
  - d/dx(sin⁻¹x) = 1/√(1−x²); d/dx(tan⁻¹x) = 1/(1+x²)
- **Implicit differentiation**: Differentiate both sides w.r.t. x, solve for dy/dx.
- **Parametric**: dy/dx = (dy/dt)/(dx/dt)
- **Logarithmic differentiation**: For y = f(x)^g(x), take ln both sides.

### Common JEE Traps
- d/dx(xˣ) requires logarithmic differentiation, not power rule.
- Second derivative: d²y/dx² for parametric requires careful computation.

---

## 4. Application of Derivatives

### Key Concepts
- **Tangent**: y − y₀ = f'(x₀)(x − x₀); **Normal**: slope = −1/f'(x₀)
- **Increasing/Decreasing**: f'(x) > 0 ⟹ increasing; f'(x) < 0 ⟹ decreasing
- **Maxima/Minima**:
  - First derivative test: Sign change of f'
  - Second derivative test: f'(c) = 0 and f''(c) < 0 ⟹ local max
- **Mean Value Theorem (MVT)**: If f continuous on [a,b] and differentiable on (a,b), ∃c ∈ (a,b) with f'(c) = [f(b)−f(a)]/(b−a)
- **Rolle's Theorem**: Special case of MVT where f(a) = f(b), so f'(c) = 0.

### Optimization Strategy for JEE
1. Identify the quantity to optimize.
2. Express it as a function of one variable.
3. Find critical points (f' = 0).
4. Verify using second derivative or boundary analysis.

---

## 5. Indefinite Integration

### Key Concepts
- **Basic**: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C (n ≠ −1); ∫1/x dx = ln|x| + C
- **Standard integrals**:
  - ∫eˣ dx = eˣ + C
  - ∫sin x dx = −cos x + C
  - ∫sec²x dx = tan x + C
  - ∫1/(1+x²) dx = tan⁻¹x + C
  - ∫1/√(1−x²) dx = sin⁻¹x + C
- **Substitution**: ∫f(g(x))g'(x) dx = ∫f(u) du where u = g(x)
- **Integration by parts**: ∫u dv = uv − ∫v du (ILATE rule: Inverse trig, Log, Algebraic, Trig, Exponential)
- **Partial fractions**: For rational functions P(x)/Q(x) where deg(P) < deg(Q).

### Special Integrals (JEE favorites)
- ∫eˣ[f(x) + f'(x)] dx = eˣf(x) + C
- ∫dx/(x² + a²) = (1/a)tan⁻¹(x/a) + C
- ∫dx/√(a² − x²) = sin⁻¹(x/a) + C
- ∫√(a² − x²) dx = (x/2)√(a² − x²) + (a²/2)sin⁻¹(x/a) + C

### Reduction Formulas
- Iₙ = ∫sinⁿx dx → Iₙ = −sinⁿ⁻¹x·cosx/n + (n−1)/n · Iₙ₋₂

---

## 6. Definite Integration & Area

### Key Concepts
- **Fundamental Theorem**: ∫ₐᵇ f(x)dx = F(b) − F(a) where F' = f
- **Properties**:
  - ∫ₐᵇ f(x)dx = −∫ᵇₐ f(x)dx
  - ∫ₐᵇ f(x)dx = ∫ₐᶜ f(x)dx + ∫ᶜᵇ f(x)dx
  - King's property: ∫₀ᵃ f(x)dx = ∫₀ᵃ f(a−x)dx
  - Queen's property: ∫₀²ᵃ f(x)dx = 2∫₀ᵃ f(x)dx if f(2a−x) = f(x), else 0
  - For even f: ∫₋ₐᵃ f(x)dx = 2∫₀ᵃ f(x)dx
  - For odd f: ∫₋ₐᵃ f(x)dx = 0
- **Leibniz Rule**: d/dx[∫ₐ₍ₓ₎ᵇ⁽ˣ⁾ f(t)dt] = f(b(x))b'(x) − f(a(x))a'(x)

### Area Under Curves
- Area between y = f(x) and x-axis from a to b: A = ∫ₐᵇ |f(x)| dx
- Area between two curves: A = ∫ₐᵇ |f(x) − g(x)| dx
- Find intersection points first, then integrate piece-wise.

---

## 7. Differential Equations

### Key Concepts
- **Order & Degree**: Order = highest derivative; Degree = power of highest derivative (only for polynomial DEs).
- **Variable separable**: dy/dx = f(x)g(y) → ∫dy/g(y) = ∫f(x)dx
- **Homogeneous DE**: dy/dx = f(y/x); substitute y = vx.
- **Linear DE**: dy/dx + P(x)y = Q(x)
  - Integrating factor: μ = e^(∫P(x)dx)
  - Solution: y · μ = ∫Q(x) · μ dx + C
- **Exact DE**: M dx + N dy = 0 where ∂M/∂y = ∂N/∂x

### Common JEE Problem Types
1. Orthogonal trajectories
2. Growth/decay: dN/dt = kN → N = N₀eᵏᵗ
3. Geometric applications (tangent/normal conditions → DE)

