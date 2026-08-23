/*
 * =========================================================
 * AI ASSISTANT — AUTHENTICATION
 * =========================================================
 *
 * Frontend authentication controller.
 *
 * Responsibilities:
 *  - Login form validation
 *  - Signup form validation
 *  - Password confirmation
 *  - Terms & conditions validation
 *  - Remember-me state
 *  - Google authentication entry point
 *
 * Backend authentication will be connected later.
 * =========================================================
 */

"use strict";


/* =========================================================
 * INITIALIZATION
 * ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    const authForm =
        document.querySelector(".auth-form");

    if (authForm) {

        authForm.addEventListener(
            "submit",
            handleAuth
        );

    }


    initializePasswordValidation();

    initializePasswordVisibility();


    /*
     * Google Identity Services loads asynchronously.
     */
    initializeGoogleWhenReady();

});


/* =========================================================
 * AUTHENTICATION ROUTER
 * ========================================================= */

/**
 * Determines whether the current page is login or signup.
 *
 * @param {SubmitEvent} event
 */
/**
 * =========================================================
 * AUTHENTICATION ROUTER
 * =========================================================
 *
 * Determines which authentication form was submitted.
 *
 * @param {SubmitEvent} event
 */
function handleAuth(event) {

    event.preventDefault();

    const form = event.currentTarget;


    /*
     * LOGIN
     */
    if (form.id === "loginForm") {

        handleLogin(form);

        return;
    }


    /*
     * SIGNUP
     */
    if (form.id === "signupForm") {

        handleSignup(form);

        return;
    }


    /*
     * FORGOT PASSWORD
     */
    if (form.id === "forgotPasswordForm") {

        handleForgotPassword(form);

        return;
    }


    /*
     * Unknown authentication form.
     */
    console.warn(
        "Unknown authentication form:",
        form.id
    );

}

/* =========================================================
 * LOGIN
 * ========================================================= */

/**
 * Handles login form submission.
 *
 * @param {HTMLFormElement} form - The login form.
 */
async function handleLogin(form) {

    const email =
        document.getElementById("email");

    const password =
        document.getElementById("password");

    const remember =
        document.getElementById("remember");

    /*
     * Safety check.
     */
    if (!email || !password) {

        console.error(
            "Login fields are missing from the page."
        );

        return;
    }


    /*
     * Clear previous validation state.
     */
    clearInputError(email);
    clearInputError(password);


    /*
     * Validate email.
     */
    if (!email.value.trim()) {

        showInputError(
            email,
            "Please enter your email."
        );

        email.focus();

        return;
    }


    /*
     * Validate email format.
     */
    if (!email.validity.valid) {

        showInputError(
            email,
            "Please enter a valid email address."
        );

        email.focus();

        return;
    }


    /*
     * Validate password.
     */
    if (!password.value) {

        showInputError(
            password,
            "Please enter your password."
        );

        password.focus();

        return;
    }


    /*
     * Build login payload.
     */
    const loginData = {

        email: email.value.trim(),

        password: password.value,

        remember: remember
            ? remember.checked
            : false

    };


    /*
     * Find the submit button from
     * the form that was submitted.
     */
    const submitButton =
        form.querySelector(".auth-submit");


    /*
     * Start loading state.
     */
    setLoginLoadingState(
        submitButton,
        true
    );


    try {

        /*
         * Frontend-only login for now.
         *
         * This will later become the real
         * backend API request.
         */
        const result = await submitLogin(loginData);
        const storage = loginData.remember
            ? localStorage
            : sessionStorage;

        storage.setItem(
            "authenticatedUser",
            JSON.stringify(result.user)
        );
        console.log(
            "Loging successful:",
            result
        );


        /*
         * Login validation succeeded.
         */
        console.log(
            "Login validation successful."
        );


        /*
         * Never log the password.
         */
        console.log({
            email: loginData.email,
            remember: loginData.remember
        });


    } catch (error) {

        /*
         * Handle unexpected login errors.
         */
        console.error(
            "Login failed:",
            error
        );


    } finally {

        /*
         * Always restore the button,
         * whether login succeeds or fails.
         */
        setLoginLoadingState(
            submitButton,
            false
        );

    }
}


/* =========================================================
 * LOGIN SUBMISSION
 * ========================================================= */

/**
 * Temporary login submission handler.
 *
 * This will eventually send:
 *
 * POST /api/auth/login
 *
 * @param {Object} loginData
 */
/**
 * Temporary frontend login simulation.
 *
 * This will be replaced by the real backend
 * API request later.
 */
async function submitLogin(loginData) {
    const response = await fetch(
        "http://127.0.0.1:8001/api/auth/login",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: loginData.email,
                password: loginData.password
            })
        }
    );

    const data = await response.json();

    // HTTP-level failure
    if (!response.ok) {
        throw new Error(
            data.detail?.[0]?.msg ||
            data.message ||
            "Login failed."
        );
    }

    // Backend authentication failure
    if (!data.success) {
        throw new Error(
            data.message ||
            "Invalid email or password."
        );
    }

    return data;
}

    /*
     * Backend integration will replace this section.
     *
     * Example future implementation:
     *
     * const response = await fetch(
     *     "/api/auth/login",
     *     {
     *         method: "POST",
     *         headers: {
     *             "Content-Type": "application/json"
     *         },
     *         body: JSON.stringify(loginData)
     *     }
     * );
     */

/* =========================================================
 * GOOGLE INITIALIZATION
 * ========================================================= */

function initializeGoogleWhenReady() {

    if (
        typeof google !== "undefined" &&
        google.accounts &&
        google.accounts.id
    ) {

        initializeGoogleAuth();

        return;
    }


    /*
     * Google library hasn't finished loading.
     * Wait a little and try again.
     */
    setTimeout(
        initializeGoogleWhenReady,
        100
    );

}


/* =========================================================
 * SIGNUP
 * ========================================================= */

/**
 * Handles signup form validation.
 *
 * Expected signup IDs:
 *
 * name
 * email
 * password
 * confirmPassword
 * password-error
 * terms
 *
 * @param {HTMLFormElement} form
 */
function handleSignup(form) {

    const name =
        document.getElementById("name");

    const email =
        document.getElementById("email");

    const password =
        document.getElementById("password");

    const confirmPassword =
        document.getElementById("confirmPassword");

    const terms =
        document.getElementById("terms");

    const passwordError =
        document.getElementById("password-error");


    /*
     * Safety check.
     */
    if (
        !name ||
        !email ||
        !password ||
        !confirmPassword
    ) {

        console.error(
            "Signup fields are missing from the page."
        );

        return;
    }


    /*
     * Clear previous errors.
     */
    clearValidationErrors(
        password,
        confirmPassword,
        passwordError
    );


    /*
     * Validate name.
     */
    if (!name.value.trim()) {

        showInputError(
            name,
            "Please enter your name."
        );

        name.focus();

        return;
    }


    /*
     * Validate email.
     */
    if (!email.value.trim()) {

        showInputError(
            email,
            "Please enter your email."
        );

        email.focus();

        return;
    }


    /*
     * Validate password length.
     */
    if (password.value.length < 8) {

        showPasswordError(
            "Password must be at least 8 characters.",
            password,
            passwordError
        );

        password.focus();

        return;
    }


    /*
     * Validate password confirmation.
     */
    if (
        password.value !==
        confirmPassword.value
    ) {

        showPasswordError(
            "Passwords do not match.",
            confirmPassword,
            passwordError
        );

        confirmPassword.focus();

        return;
    }


    /*
     * Validate terms.
     */
    if (terms && !terms.checked) {

        showTermsError(terms);

        return;
    }


    /*
     * Build signup payload.
     *
     * Never include the password in console logs.
     */
    const signupData = {

        name: name.value.trim(),

        email: email.value.trim(),

        password: password.value

    };


    /*
     * Submit signup.
     */
    submitSignup(signupData);

}


/* =========================================================
 * SIGNUP SUBMISSION
 * ========================================================= */

/**
 * Temporary signup submission handler.
 *
 * Backend API will be connected later.
 *
 * @param {Object} signupData
 */
async function submitSignup(signupData) {

    /*
     * Never log passwords.
     */

    console.log(
        "Signup validation successful."
    );

    console.log({
        name: signupData.name,
        email: signupData.email
    });


    /*
     * Future:
     *
     * POST /api/auth/signup
     */

}


/* =========================================================
 * PASSWORD VALIDATION
 * ========================================================= */

/**
 * Adds live validation to confirmPassword.
 */
function initializePasswordValidation() {

    const confirmPassword =
        document.getElementById(
            "confirmPassword"
        );

    /*
     * Login page does not have this field.
     */
    if (!confirmPassword) {
        return;
    }


    confirmPassword.addEventListener(
        "input",
        () => {

            const passwordError =
                document.getElementById(
                    "password-error"
                );


            /*
             * Remove previous error.
             */
            if (passwordError) {

                clearError(
                    passwordError
                );
            }


            /*
             * Remove visual error state.
             */
            clearInputError(
                confirmPassword
            );

        }
    );

}


/* =========================================================
 * INPUT ERROR HANDLING
 * ========================================================= */

/**
 * Shows an error on an input.
 *
 * @param {HTMLInputElement} input
 * @param {string} message
 */
function showInputError(input, message) {

    /*
     * Your existing CSS uses input-error.
     */
    input.classList.add(
        "input-error"
    );


    /*
     * Use the browser's native validation message
     * as a fallback without modifying the HTML.
     */
    input.setCustomValidity(
        message
    );

}


/**
 * Removes an input error.
 *
 * @param {HTMLInputElement} input
 */
function clearInputError(input) {

    if (!input) {
        return;
    }

    input.classList.remove(
        "input-error"
    );

    input.setCustomValidity("");

}


/* =========================================================
 * PASSWORD ERROR
 * ========================================================= */

/**
 * Displays password-related validation error.
 *
 * @param {string} message
 * @param {HTMLInputElement} input
 * @param {HTMLElement} errorElement
 */
function showPasswordError(
    message,
    input,
    errorElement
) {

    /*
     * Display message using the existing
     * password-error element.
     */
    if (errorElement) {

        errorElement.textContent =
            message;

        errorElement.classList.add(
            "visible"
        );
    }


    /*
     * Apply existing input error styling.
     */
    if (input) {

        input.classList.add(
            "input-error"
        );

        input.setCustomValidity(
            message
        );
    }

}


/* =========================================================
 * CLEAR PASSWORD ERRORS
 * ========================================================= */

/**
 * Clears password validation state.
 *
 * @param {HTMLInputElement} password
 * @param {HTMLInputElement} confirmPassword
 * @param {HTMLElement} errorElement
 */
function clearValidationErrors(
    password,
    confirmPassword,
    errorElement
) {

    clearInputError(password);

    clearInputError(confirmPassword);

    clearError(errorElement);

}


/* =========================================================
 * GENERIC ERROR
 * ========================================================= */

/**
 * Shows a field error.
 *
 * @param {HTMLElement} errorElement
 * @param {string} message
 */
function showError(
    errorElement,
    message
) {

    if (!errorElement) {
        return;
    }

    errorElement.textContent =
        message;

    errorElement.classList.add(
        "visible"
    );

}


/**
 * Clears a field error.
 *
 * @param {HTMLElement} errorElement
 */
function clearError(errorElement) {

    if (!errorElement) {
        return;
    }

    errorElement.textContent = "";

    errorElement.classList.remove(
        "visible"
    );

}


/* =========================================================
 * TERMS & CONDITIONS
 * ========================================================= */

/**
 * Handles terms checkbox validation.
 *
 * @param {HTMLInputElement} terms
 */
function showTermsError(terms) {

    /*
     * Use the existing styling class.
     */
    terms.classList.add(
        "input-error"
    );


    /*
     * Native validation message.
     */
    terms.setCustomValidity(
        "You must agree to the Terms and Conditions."
    );


    terms.reportValidity();


    /*
     * Remove custom validity once checked.
     */
    terms.addEventListener(
        "change",
        () => {

            if (terms.checked) {

                terms.classList.remove(
                    "input-error"
                );

                terms.setCustomValidity("");

            }

        },
        {
            once: true
        }
    );

}


/* =========================================================
 * GOOGLE AUTHENTICATION
 * ========================================================= */

/**
 * Google OAuth Client ID.
 *
 * Replace this with your actual Google Web Client ID.
 */
const GOOGLE_CLIENT_ID =
    "387036885060-snlc449ir2iri9aua9i9p0ia8oi4h0s7.apps.googleusercontent.com";


/**
 * Initializes Google authentication.
 */
function initializeGoogleAuth() {

    /*
     * Google Identity Services may still be
     * loading because its script is async.
     */
    if (
        typeof google === "undefined" ||
        !google.accounts ||
        !google.accounts.id
    ) {

        console.warn(
            "Google Identity Services is not loaded yet."
        );

        return;
    }


    /*
     * Configure Google Identity Services.
     */
    google.accounts.id.initialize({

        client_id: GOOGLE_CLIENT_ID,

        callback:
            handleGoogleCredential

    });


    /*
     * Login page.
     */
    const googleLogin =
        document.getElementById(
            "googleLogin"
        );


    if (googleLogin) {

        google.accounts.id.renderButton(
            googleLogin,
            {
                type: "standard",
                theme: "outline",
                size: "large",
                text: "signin_with",
                shape: "rectangular",
                logo_alignment: "left",
                width: 360
            }
        );

    }


    /*
     * Signup page.
     */
    const googleSignup =
        document.getElementById(
            "googleSignup"
        );


    if (googleSignup) {

        google.accounts.id.renderButton(
            googleSignup,
            {
                type: "standard",
                theme: "outline",
                size: "large",
                text: "signup_with",
                shape: "rectangular",
                logo_alignment: "left",
                width: 360
            }
        );

    }

}


/* =========================================================
 * GOOGLE CREDENTIAL
 * ========================================================= */

/**
 * Handles the credential returned by Google.
 *
 * @param {Object} response
 */
function handleGoogleCredential(response) {

    if (
        !response ||
        !response.credential
    ) {

        console.error(
            "Google authentication returned no credential."
        );

        return;
    }


    /*
     * The credential is an ID token.
     *
     * IMPORTANT:
     * Do NOT trust decoded client-side data
     * for authentication.
     *
     * The backend must verify this token.
     */
    console.log(
        "Google authentication successful."
    );


    /*
     * Temporary frontend-only inspection.
     *
     * We will replace this with:
     *
     * POST /api/auth/google
     *
     * once your backend authentication
     * endpoint is ready.
     */
    console.log(
        "Google credential received."
    );


    /*
     * DO NOT do this in production:
     *
     * console.log(response.credential);
     *
     * The ID token should be sent securely
     * to your backend instead.
     */


    submitGoogleCredential(
        response.credential
    );

}


/* =========================================================
 * GOOGLE BACKEND SUBMISSION
 * ========================================================= */

/**
 * Temporary Google authentication submission.
 *
 * This will eventually send the Google ID token
 * to the backend.
 *
 * @param {string} credential
 */
async function submitGoogleCredential(
    credential
) {

    /*
     * Temporary frontend implementation.
     */
    console.log(
        "Google credential ready for backend."
    );


    /*
     * Future backend implementation:
     *
     * const response = await fetch(
     *     "/api/auth/google",
     *     {
     *         method: "POST",
     *
     *         headers: {
     *             "Content-Type":
     *                 "application/json"
     *         },
     *
     *         body: JSON.stringify({
     *             credential
     *         })
     *     }
     * );
     *
     * const data =
     *     await response.json();
     *
     * if (!response.ok) {
     *
     *     throw new Error(
     *         data.message ||
     *         "Google authentication failed."
     *     );
     * }
     *
     * window.location.href =
     *     "dashboard.html";
     */
}


/* =========================================================
 * GOOGLE LOGIN
 * ========================================================= */

function handleGoogleLogin() {

    console.log(
        "Google login selected."
    );


    /*
     * Future:
     *
     * Start Google Identity Services.
     *
     * Do NOT manually collect Google passwords.
     */

}


/* =========================================================
 * GOOGLE SIGNUP
 * ========================================================= */

function handleGoogleSignup() {

    console.log(
        "Google signup selected."
    );


    /*
     * Future:
     *
     * Google OAuth / Identity Services.
     */

}


/* =========================================================
 * EXPORTS
 * =========================================================
 *
 * No exports are required because this script runs
 * directly in the browser.
 * ========================================================= */
/* =========================================================
 * PASSWORD VISIBILITY
 * ========================================================= */

/**
 * Adds a show/hide button to password fields.
 */
/**
 * Adds show/hide password buttons to all password inputs.
 */
function initializePasswordVisibility() {

    const passwordFields = document.querySelectorAll(
        'input[type="password"]'
    );

    passwordFields.forEach((passwordInput) => {

        /*
         * Prevent duplicate buttons if the function
         * gets called more than once.
         */
        if (
            passwordInput.parentElement.classList.contains(
                "password-input-wrapper"
            )
        ) {
            return;
        }


        /*
         * Create a wrapper around the password input.
         *
         * This makes the button position relative
         * to the input itself.
         */
        const wrapper = document.createElement("div");

        wrapper.className =
            "password-input-wrapper";


        /*
         * Position the wrapper relative to the
         * surrounding form.
         */
        wrapper.style.position = "relative";
        wrapper.style.width = "100%";


        /*
         * Insert the wrapper before the input.
         */
        passwordInput.parentNode.insertBefore(
            wrapper,
            passwordInput
        );


        /*
         * Move the password input inside
         * the new wrapper.
         */
        wrapper.appendChild(
            passwordInput
        );


        /*
         * Create the toggle button.
         */
        const toggleButton =
            document.createElement("button");


        /*
         * Important:
         * This must NOT submit the form.
         */
        toggleButton.type = "button";


        /*
         * Use the existing password-toggle
         * CSS class.
         */
        toggleButton.className =
            "password-toggle";


        /*
         * Accessibility.
         */
        toggleButton.setAttribute(
            "aria-label",
            "Show password"
        );

        toggleButton.setAttribute(
            "title",
            "Show password"
        );


        /*
         * Initial icon.
         */
        toggleButton.textContent = "◉";


        /*
         * Toggle password visibility.
         */
        toggleButton.addEventListener(
            "click",
            () => {

                const isHidden =
                    passwordInput.type === "password";


                /*
                 * Change the input type.
                 */
                passwordInput.type =
                    isHidden
                        ? "text"
                        : "password";


                /*
                 * Change icon.
                 */
                toggleButton.textContent =
                    isHidden
                        ? "◌"
                        : "◉";


                /*
                 * Update accessibility text.
                 */
                toggleButton.setAttribute(
                    "aria-label",
                    isHidden
                        ? "Hide password"
                        : "Show password"
                );


                toggleButton.setAttribute(
                    "title",
                    isHidden
                        ? "Hide password"
                        : "Show password"
                );

            }
        );


        /*
         * Add the button inside the wrapper.
         */
        wrapper.appendChild(
            toggleButton
        );

    });

}

/**
 * Sets the login button to a loading state.
 *
 * @param {HTMLButtonElement} button - The submit button.
 * @param {boolean} loading - Whether the button is loading.
 */
function setLoginLoadingState(button, loading) {

    if (!button) {
        return;
    }

    if (loading) {

        /*
         * Prevent multiple submissions.
         */
        button.disabled = true;

        /*
         * Tell assistive technologies that
         * the button is currently busy.
         */
        button.setAttribute(
            "aria-busy",
            "true"
        );

        /*
         * Save the original content so we can
         * restore it later.
         */
        if (!button.dataset.originalContent) {
            button.dataset.originalContent =
                button.innerHTML;
        }

        /*
         * Loading UI.
         */
        button.innerHTML = `
            <span class="auth-loading">
                <span class="loading-spinner"></span>
                Signing in...
            </span>
        `;

    } else {

        /*
         * Re-enable the button.
         */
        button.disabled = false;

        /*
         * Remove the busy state.
         */
        button.removeAttribute(
            "aria-busy"
        );

        /*
         * Restore original button content.
         */
        if (button.dataset.originalContent) {
            button.innerHTML =
                button.dataset.originalContent;
        }

    }
}

/**
 * Handles the forgot-password form.
 *
 * Currently simulates the password-reset request.
 * The real API will be connected later.
 *
 * @param {HTMLFormElement} form - The reset form.
 */
async function handleForgotPassword(form) {

    const email =
        document.getElementById("resetEmail");

    const submitButton =
        form.querySelector(".auth-submit");

    const successMessage =
        document.getElementById("resetSuccess");


    /*
     * Safety check.
     */
    if (!email || !submitButton) {

        console.error(
            "Forgot-password fields are missing."
        );

        return;
    }


    /*
     * Clear previous validation state.
     */
    clearInputError(email);


    /*
     * Validate empty email.
     */
    if (!email.value.trim()) {

        showInputError(
            email,
            "Please enter your email."
        );

        email.focus();

        return;
    }


    /*
     * Validate email format.
     */
    if (!email.validity.valid) {

        showInputError(
            email,
            "Please enter a valid email address."
        );

        email.focus();

        return;
    }


    /*
     * Start loading state.
     */
    setLoginLoadingState(
        submitButton,
        true
    );


    try {

        /*
         * Temporary simulated request.
         */
        await new Promise((resolve) => {

            setTimeout(
                resolve,
                1500
            );

        });


        console.log(
            "Password reset request submitted."
        );

        console.log({
            email: email.value.trim()
        });


        /*
         * Hide the form.
         */
        form.hidden = true;


        /*
         * Show success message.
         */
        if (successMessage) {

            successMessage.hidden = false;

        }


    } catch (error) {

        console.error(
            "Password reset failed:",
            error
        );


    } finally {

        /*
         * Restore button state.
         */
        setLoginLoadingState(
            submitButton,
            false
        );

    }

}

