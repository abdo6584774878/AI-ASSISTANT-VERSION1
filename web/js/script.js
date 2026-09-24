/* =========================================================
   VEYRA — LANDING PAGE INTERACTION ENGINE
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    const body = document.body;
    const reducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    /* =====================================================
       PAGE LOAD
       ===================================================== */

    body.classList.add("page-loaded");


    /* =====================================================
       NAVBAR
       ===================================================== */

    const navbar = document.querySelector(".navbar");

    function updateNavbar() {
        if (!navbar) return;

        navbar.classList.toggle("scrolled", window.scrollY > 40);
    }

    window.addEventListener("scroll", updateNavbar, {
        passive: true
    });

    updateNavbar();


    /* =====================================================
       SMOOTH ANCHOR SCROLLING
       ===================================================== */

    document.querySelectorAll('a[href^="#"]').forEach((link) => {
        link.addEventListener("click", (event) => {
            const targetId = link.getAttribute("href");

            if (!targetId || targetId === "#") return;

            const target = document.querySelector(targetId);

            if (!target) return;

            event.preventDefault();

            target.scrollIntoView({
                behavior: reducedMotion ? "auto" : "smooth",
                block: "start"
            });
        });
    });


    /* =====================================================
       AMBIENT PARTICLES
       ===================================================== */

    const particleLayer = document.createElement("div");
    particleLayer.className = "ambient-particles";

    body.prepend(particleLayer);

    const particleCount = window.innerWidth < 700 ? 24 : 50;

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement("span");

        particle.className = "ambient-particle";

        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;
        particle.style.animationDelay = `${Math.random() * 8}s`;
        particle.style.animationDuration =
            `${5 + Math.random() * 8}s`;

        const size = 1 + Math.random() * 2;

        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;

        particleLayer.appendChild(particle);
    }


    /* =====================================================
       MOUSE LIGHT / PARALLAX
       ===================================================== */

    if (!reducedMotion) {
        let mouseX = 0;
        let mouseY = 0;

        let currentX = 0;
        let currentY = 0;

        window.addEventListener("mousemove", (event) => {
            mouseX =
                (event.clientX / window.innerWidth - 0.5) * 2;

            mouseY =
                (event.clientY / window.innerHeight - 0.5) * 2;

            document.documentElement.style.setProperty(
                "--mouse-x",
                `${event.clientX}px`
            );

            document.documentElement.style.setProperty(
                "--mouse-y",
                `${event.clientY}px`
            );
        });

        function animateMouse() {
            currentX += (mouseX - currentX) * 0.05;
            currentY += (mouseY - currentY) * 0.05;

            document.documentElement.style.setProperty(
                "--parallax-x",
                currentX
            );

            document.documentElement.style.setProperty(
                "--parallax-y",
                currentY
            );

            requestAnimationFrame(animateMouse);
        }

        animateMouse();
    }


    /* =====================================================
       SCROLL REVEAL
       ===================================================== */

    const revealElements = document.querySelectorAll(
        ".section-heading, " +
        ".feature-card, " +
        ".security-analyzer-heading, " +
        ".security-workstation, " +
        ".workflow-step, " +
        ".customization-content, " +
        ".settings-preview, " +
        ".cta"
    );

    if (reducedMotion) {
        revealElements.forEach((element) => {
            element.classList.add("revealed");
        });
    } else {
        const revealObserver = new IntersectionObserver(
            (entries, observer) => {
                entries.forEach((entry) => {
                    if (!entry.isIntersecting) return;

                    entry.target.classList.add("revealed");

                    observer.unobserve(entry.target);
                });
            },
            {
                threshold: 0.12,
                rootMargin: "0px 0px -60px 0px"
            }
        );

        revealElements.forEach((element) => {
            element.classList.add("reveal");

            revealObserver.observe(element);
        });
    }


    /* =====================================================
       FEATURE CARD STAGGER
       ===================================================== */

    document.querySelectorAll(".feature-card").forEach(
        (card, index) => {
            card.style.setProperty(
                "--card-delay",
                `${index * 90}ms`
            );
        }
    );


    /* =====================================================
       3D CARD TILT
       ===================================================== */

    if (!reducedMotion) {
        const tiltElements = document.querySelectorAll(
            ".feature-card, " +
            ".assistant-preview, " +
            ".settings-preview, " +
            ".agent-card, " +
            ".policy-card"
        );

        tiltElements.forEach((element) => {
            element.addEventListener("mousemove", (event) => {
                const rect = element.getBoundingClientRect();

                const x =
                    (event.clientX - rect.left) /
                    rect.width;

                const y =
                    (event.clientY - rect.top) /
                    rect.height;

                const rotateX = (0.5 - y) * 5;
                const rotateY = (x - 0.5) * 5;

                element.style.setProperty(
                    "--tilt-x",
                    `${rotateX}deg`
                );

                element.style.setProperty(
                    "--tilt-y",
                    `${rotateY}deg`
                );

                element.classList.add("tilting");
            });

            element.addEventListener("mouseleave", () => {
                element.style.setProperty(
                    "--tilt-x",
                    "0deg"
                );

                element.style.setProperty(
                    "--tilt-y",
                    "0deg"
                );

                element.classList.remove("tilting");
            });
        });
    }


    /* =====================================================
       HERO PRODUCT PREVIEW
       ===================================================== */

    const preview = document.querySelector(
        ".assistant-preview"
    );

    if (preview && !reducedMotion) {
        const messages = preview.querySelectorAll(".message");

        messages.forEach((message, index) => {
            message.style.setProperty(
                "--message-delay",
                `${700 + index * 650}ms`
            );
        });

        const toolStatus = preview.querySelector(
            ".tool-status"
        );

        if (toolStatus) {
            toolStatus.classList.add("live");
        }
    }


    /* =====================================================
       SECURITY SCORE
       ===================================================== */

    const scoreElement = document.querySelector(
        ".score-ring span"
    );

    const scoreRing = document.querySelector(
        ".score-ring"
    );

    if (scoreElement && scoreRing) {
        const targetScore = Number(
            scoreElement.textContent.trim()
        ) || 0;

        scoreElement.textContent = "0";

        const scoreObserver = new IntersectionObserver(
            (entries, observer) => {
                entries.forEach((entry) => {
                    if (!entry.isIntersecting) return;

                    observer.unobserve(entry.target);

                    if (reducedMotion) {
                        scoreElement.textContent =
                            targetScore;

                        scoreRing.style.setProperty(
                            "--score-progress",
                            `${targetScore * 3.6}deg`
                        );

                        return;
                    }

                    let currentScore = 0;
                    const duration = 1400;
                    const start = performance.now();

                    function animateScore(now) {
                        const progress = Math.min(
                            (now - start) / duration,
                            1
                        );

                        const eased =
                            1 - Math.pow(1 - progress, 3);

                        currentScore = Math.round(
                            targetScore * eased
                        );

                        scoreElement.textContent =
                            currentScore;

                        scoreRing.style.setProperty(
                            "--score-progress",
                            `${currentScore * 3.6}deg`
                        );

                        if (progress < 1) {
                            requestAnimationFrame(
                                animateScore
                            );
                        }
                    }

                    requestAnimationFrame(animateScore);
                });
            },
            {
                threshold: 0.5
            }
        );

        scoreObserver.observe(scoreRing);
    }


    /* =====================================================
       SECURITY FINDINGS
       ===================================================== */

    const findings = document.querySelectorAll(
        ".security-finding"
    );

    if (findings.length) {
        const findingsContainer =
            document.querySelector(
                ".security-findings"
            );

        if (findingsContainer) {
            const findingsObserver =
                new IntersectionObserver(
                    (entries, observer) => {
                        entries.forEach((entry) => {
                            if (!entry.isIntersecting)
                                return;

                            observer.unobserve(
                                entry.target
                            );

                            findings.forEach(
                                (finding, index) => {
                                    finding.style.setProperty(
                                        "--finding-delay",
                                        `${index * 180}ms`
                                    );

                                    finding.classList.add(
                                        "finding-visible"
                                    );
                                }
                            );
                        });
                    },
                    {
                        threshold: 0.3
                    }
                );

            findingsObserver.observe(
                findingsContainer
            );
        }
    }


    /* =====================================================
       SECURITY POLICY ANIMATION
       ===================================================== */

    const policyRules = document.querySelectorAll(
        ".policy-rule"
    );

    if (policyRules.length) {
        const policyCard =
            document.querySelector(".policy-card");

        if (policyCard) {
            const policyObserver =
                new IntersectionObserver(
                    (entries, observer) => {
                        entries.forEach((entry) => {
                            if (!entry.isIntersecting)
                                return;

                            observer.unobserve(
                                entry.target
                            );

                            policyRules.forEach(
                                (rule, index) => {
                                    rule.style.setProperty(
                                        "--policy-delay",
                                        `${index * 160}ms`
                                    );

                                    rule.classList.add(
                                        "policy-visible"
                                    );
                                }
                            );
                        });
                    },
                    {
                        threshold: 0.35
                    }
                );

            policyObserver.observe(policyCard);
        }
    }


    /* =====================================================
       WORKFLOW DATA FLOW
       ===================================================== */

    document.querySelectorAll(
        ".workflow-line"
    ).forEach((line) => {
        if (!reducedMotion) {
            line.classList.add("flowing");
        }
    });


    /* =====================================================
       SETTINGS INTERACTION
       ===================================================== */

    document.querySelectorAll(
        ".toggle"
    ).forEach((toggle) => {
        toggle.addEventListener("click", () => {
            toggle.classList.toggle("active");

            const state =
                toggle.classList.contains("active");

            toggle.setAttribute(
                "aria-pressed",
                String(state)
            );
        });

        toggle.setAttribute(
            "role",
            "button"
        );

        toggle.setAttribute(
            "tabindex",
            "0"
        );

        toggle.addEventListener(
            "keydown",
            (event) => {
                if (
                    event.key === "Enter" ||
                    event.key === " "
                ) {
                    event.preventDefault();
                    toggle.click();
                }
            }
        );
    });


    /* =====================================================
       MAGNETIC BUTTON EFFECT
       ===================================================== */

    if (!reducedMotion) {
        document.querySelectorAll(
            ".primary-button, .nav-button"
        ).forEach((button) => {
            button.addEventListener(
                "mousemove",
                (event) => {
                    const rect =
                        button.getBoundingClientRect();

                    const x =
                        event.clientX -
                        rect.left -
                        rect.width / 2;

                    const y =
                        event.clientY -
                        rect.top -
                        rect.height / 2;

                    button.style.transform =
                        `translate(${x * 0.08}px, ${y * 0.08}px)`;
                }
            );

            button.addEventListener(
                "mouseleave",
                () => {
                    button.style.transform = "";
                }
            );
        });
    }


    /* =====================================================
       ACTIVE NAV SECTION
       ===================================================== */

    const sections = document.querySelectorAll(
        "main section[id]"
    );

    const navLinks = document.querySelectorAll(
        ".nav-links a[href^='#']"
    );

    if (sections.length && navLinks.length) {
        const sectionObserver =
            new IntersectionObserver(
                (entries) => {
                    entries.forEach((entry) => {
                        if (!entry.isIntersecting)
                            return;

                        const id = entry.target.id;

                        navLinks.forEach((link) => {
                            link.classList.toggle(
                                "active",
                                link.getAttribute(
                                    "href"
                                ) === `#${id}`
                            );
                        });
                    });
                },
                {
                    threshold: 0.35
                }
            );

        sections.forEach((section) => {
            sectionObserver.observe(section);
        });
    }


    /* =====================================================
       CURSOR GLOW ON CARDS
       ===================================================== */

    if (!reducedMotion) {
        document.querySelectorAll(
            ".feature-card, " +
            ".security-finding, " +
            ".policy-card, " +
            ".agent-card"
        ).forEach((card) => {
            card.addEventListener(
                "mousemove",
                (event) => {
                    const rect =
                        card.getBoundingClientRect();

                    const x =
                        event.clientX - rect.left;

                    const y =
                        event.clientY - rect.top;

                    card.style.setProperty(
                        "--cursor-x",
                        `${x}px`
                    );

                    card.style.setProperty(
                        "--cursor-y",
                        `${y}px`
                    );
                }
            );
        });
    }


    /* =====================================================
       SECURITY STATUS PULSE
       ===================================================== */

    const securityDot = document.querySelector(
        ".security-status-dot"
    );

    if (securityDot && !reducedMotion) {
        securityDot.classList.add(
            "security-pulse"
        );
    }


    /* =====================================================
       ASSISTANT STATUS PULSE
       ===================================================== */

    document.querySelectorAll(
        ".status-dot"
    ).forEach((dot) => {
        if (!reducedMotion) {
            dot.classList.add("status-pulse");
        }
    });


    /* =====================================================
       BUTTON RIPPLE
       ===================================================== */

    document.querySelectorAll(
        "button, .primary-button, .secondary-button, .nav-button"
    ).forEach((element) => {
        element.addEventListener("click", (event) => {
            if (reducedMotion) return;

            const rect =
                element.getBoundingClientRect();

            const ripple =
                document.createElement("span");

            ripple.className = "button-ripple";

            ripple.style.left =
                `${event.clientX - rect.left}px`;

            ripple.style.top =
                `${event.clientY - rect.top}px`;

            element.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 700);
        });
    });


    /* =====================================================
       CONSOLE BRANDING
       ===================================================== */

    console.log(
        "%cVEYRA",
        "font-size: 28px; font-weight: 800; letter-spacing: 8px;"
    );

    console.log(
        "%cIntelligence, your way.",
        "font-size: 13px; opacity: .65;"
    );
});

/* =========================================================
   VEYRA — NAVBAR CONTROLLER
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    const navbar = document.querySelector(".navbar");
    const navDock = document.querySelector(".nav-dock");
    const navLinks = document.querySelectorAll(".nav-link");
    const indicator = document.querySelector(".nav-indicator");

    if (!navbar) return;


    /* -----------------------------------------
       SCROLL TRANSFORMATION
       ----------------------------------------- */

    const updateNavbar = () => {
        navbar.classList.toggle("scrolled", window.scrollY > 80);
    };

    updateNavbar();

    window.addEventListener("scroll", updateNavbar, {
        passive: true
    });


    /* -----------------------------------------
       MOVING ACTIVE INDICATOR
       ----------------------------------------- */

    const moveIndicator = (link) => {

        if (!indicator || !navDock || !link) return;

        const dockRect = navDock.getBoundingClientRect();
        const linkRect = link.getBoundingClientRect();

        indicator.style.width = `${linkRect.width - 20}px`;

        indicator.style.transform =
            `translateX(${linkRect.left - dockRect.left + 10}px)`;
    };


    const activeLink =
        document.querySelector(".nav-link.active");

    if (activeLink) {
        requestAnimationFrame(() => {
            moveIndicator(activeLink);
        });
    }


    navLinks.forEach(link => {

        link.addEventListener("mouseenter", () => {
            moveIndicator(link);
        });

        link.addEventListener("mouseleave", () => {

            const current =
                document.querySelector(".nav-link.active");

            if (current) {
                moveIndicator(current);
            }
        });

    });


    /* -----------------------------------------
       ACTIVE SECTION TRACKING
       ----------------------------------------- */

    const sections = document.querySelectorAll(
        "section[id]"
    );

    if ("IntersectionObserver" in window) {

        const observer = new IntersectionObserver(
            entries => {

                entries.forEach(entry => {

                    if (!entry.isIntersecting) return;

                    const id = entry.target.id;

                    navLinks.forEach(link => {

                        const href =
                            link.getAttribute("href");

                        if (href === `#${id}`) {

                            navLinks.forEach(l =>
                                l.classList.remove("active")
                            );

                            link.classList.add("active");

                            moveIndicator(link);
                        }
                    });

                });

            },
            {
                threshold: 0.35
            }
        );

        sections.forEach(section =>
            observer.observe(section)
        );
    }


    /* -----------------------------------------
       NAVBAR MOUSE PARALLAX
       ----------------------------------------- */

    if (window.matchMedia(
        "(pointer: fine)"
    ).matches) {

        navbar.addEventListener("mousemove", event => {

            const rect =
                navbar.getBoundingClientRect();

            const x =
                (event.clientX - rect.left) / rect.width - .5;

            const y =
                (event.clientY - rect.top) / rect.height - .5;

            navDock.style.transform =
                `translateY(${y * 2}px)`;

        });

        navbar.addEventListener("mouseleave", () => {

            navDock.style.transform =
                "translateY(0)";

        });
    }

});

document.addEventListener("DOMContentLoaded", () => {

    const howSystem = document.querySelector(".how-system");

    if (!howSystem) return;

    const observer = new IntersectionObserver(
        (entries) => {

            entries.forEach((entry) => {

                if (entry.isIntersecting) {

                    howSystem.classList.add("how-active");

                }

            });

        },
        {
            threshold: 0.35
        }
    );

    observer.observe(howSystem);


    /* =========================================
       MOUSE PARALLAX
       ========================================= */

    howSystem.addEventListener("mousemove", (event) => {

        const rect = howSystem.getBoundingClientRect();

        const x =
            (event.clientX - rect.left) /
            rect.width -
            0.5;

        const y =
            (event.clientY - rect.top) /
            rect.height -
            0.5;

        const center = howSystem.querySelector(".how-center");

        if (center) {

            center.style.transform = `
                translate(
                    ${x * 8}px,
                    ${y * 8}px
                )
                scale(1)
            `;

        }

    });


    howSystem.addEventListener("mouseleave", () => {

        const center = howSystem.querySelector(".how-center");

        if (center) {

            center.style.transform =
                "translate(0, 0) scale(1)";

        }

    });

});