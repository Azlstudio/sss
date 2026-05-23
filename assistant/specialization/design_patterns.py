class DesignPatterns:
    """UI/UX and code design patterns."""

    SYSTEM_PROMPT = """You are an expert in clean, minimalist design and software architecture:
- UI/UX design principles
- Clean code architecture
- Design patterns (singleton, observer, factory, etc.)
- Performance optimization
- Security by design
- Scalability patterns
- Code organization and structure

Recommend solutions that are minimal, professional, and maintainable."""

    PATTERNS = {
        'ui_ux_principles': {
            'minimalism': """
Core principles:
- Remove unnecessary elements
- Use whitespace effectively
- Choose typography carefully
- Limit color palette (2-3 main colors + accents)
- Focus on essential information
- Avoid animations unless purposeful

Benefits:
- Faster load times
- Better user focus
- Easier to maintain
- More professional appearance""",

            'hierarchy': """
Visual hierarchy guides user attention:
- Size: Important elements larger
- Color: Highlight key actions
- Position: Critical items at top/center
- Spacing: Group related elements
- Weight: Use font weights for emphasis

Implementation:
- Primary action (CTA): Bold, contrasting color
- Secondary actions: Neutral, smaller
- Information: Subtle, muted colors""",

            'responsive_design': """
Mobile-first approach:
1. Design for smallest screen first
2. Use flexible grid systems
3. Optimize touch targets (48px minimum)
4. Test on actual devices
5. Use relative units (rem, em, %)

Breakpoints:
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px""",

            'accessibility': """
WCAG 2.1 Guidelines:
- Color contrast ratio ≥ 4.5:1
- Keyboard navigation support
- Screen reader compatibility
- Clear focus indicators
- Form labels and error messages
- Alt text for images

Benefits:
- Reach more users
- Better SEO
- Improved usability overall"""
        },

        'architecture_patterns': {
            'mvc': """
Model-View-Controller:
- Model: Data and business logic
- View: UI presentation
- Controller: User interaction handling

Benefits:
- Separation of concerns
- Easy to test
- Scalable
- Maintainable

Implementation:
- Model: Database queries, validations
- View: HTML/CSS/Components
- Controller: Route handlers, business logic""",

            'observer': """
Observer Pattern:
- Subject notifies multiple observers
- Loose coupling between components
- Event-driven architecture

Usage:
- DOM events
- State management
- Real-time updates

Implementation:
- Event emitter base class
- Subscribe/unsubscribe methods
- Notify all listeners on change""",

            'singleton': """
Singleton Pattern:
- Only one instance exists
- Global access point
- Lazy initialization

Use cases:
- Configuration managers
- Loggers
- Database connections

Cautions:
- Can be hard to test
- Thread safety concerns
- Use sparingly""",

            'factory': """
Factory Pattern:
- Create objects without specifying classes
- Encapsulate object creation
- Easy to extend

Benefits:
- Flexible object creation
- Easy to add new types
- Centralized creation logic

Example:
- Database factory (MySQL, SQLite, etc.)
- Logger factory (File, Console, etc.)"""
        },

        'code_quality': {
            'dry': """
Don't Repeat Yourself:
- Extract common code to functions
- Use constants instead of magic numbers
- Create reusable components

Violation example:
```
// BAD
const price = quantity * 100;
const discount = quantity * 100 * 0.1;
const total = quantity * 100 - discount;
```

Better approach:
```
const UNIT_PRICE = 100;
const DISCOUNT_RATE = 0.1;
const price = quantity * UNIT_PRICE;
const discount = price * DISCOUNT_RATE;
const total = price - discount;
```""",

            'solid': """
SOLID Principles:
- Single Responsibility: One job per class
- Open/Closed: Open for extension, closed for modification
- Liskov Substitution: Subclasses replaceable
- Interface Segregation: Specific interfaces
- Dependency Inversion: Depend on abstractions

Implementation benefits:
- More maintainable code
- Easier testing
- Better modularity""",

            'naming': """
Good naming conventions:
- Variables: noun + descriptor (userCount, isActive)
- Functions: verb + action (getUserData, validateEmail)
- Classes: PascalCase singular (User, DatabaseConnection)
- Constants: UPPER_SNAKE_CASE (MAX_RETRIES)
- Avoid: single letters (except loops), unclear abbreviations

Example:
- GOOD: calculateTotalPrice
- BAD: calc, getTP, computeValue""",

            'documentation': """
Effective documentation:
- Code comments: WHY, not WHAT
- Function docstrings: Purpose, params, return
- README: Setup, usage, architecture overview
- ARCHITECTURE.md: System design decisions

Example:
```
// Calculate discounted price with bulk rates
// Applies tiered discounts based on quantity ranges
function getPriceWithDiscount(quantity, basePrice) {
    // Bulk tier: 50+ units = 10% off
    // ...logic here...
}
```"""
        }
    }

    @staticmethod
    def get_principle(principle: str) -> str:
        """Get design principle explanation."""
        for category in DesignPatterns.PATTERNS.values():
            if principle.lower() in category:
                return category[principle.lower()]
        return "Principle not found."

    @staticmethod
    def list_all_patterns() -> dict:
        """List all available patterns."""
        return DesignPatterns.PATTERNS

    @staticmethod
    def get_pattern_category(category: str) -> dict:
        """Get all patterns in a category."""
        return DesignPatterns.PATTERNS.get(category, {})
