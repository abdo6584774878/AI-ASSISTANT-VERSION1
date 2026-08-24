console.log("🔥 DASHBOARD.JS LOADED");
document.addEventListener("DOMContentLoaded", () => {
    console.log("🔥 DASHBOARD DOM READY");
    const switchOptions = document.querySelectorAll(
        ".product-switch-option"
    );

    const chatbotNav = document.getElementById("chatbot-nav");
    const securityNav = document.getElementById("security-nav");

    const chatbotWorkspace =
        document.getElementById("chatbot-workspace");

    const securityWorkspace =
        document.getElementById("security-workspace");

    const workspaceTitle =
        document.getElementById("workspace-title");


    function switchWorkspace(workspace) {

        const isChatbot = workspace === "chatbot";

        /* Switch buttons */

        switchOptions.forEach(option => {

            const active =
                option.dataset.workspace === workspace;

            option.classList.toggle("active", active);

            option.setAttribute(
                "aria-selected",
                active ? "true" : "false"
            );
        });


        /* Sidebar */

        chatbotNav.classList.toggle(
            "hidden",
            !isChatbot
        );

        securityNav.classList.toggle(
            "hidden",
            isChatbot
        );


        /* Main workspace */

        chatbotWorkspace.classList.toggle(
            "hidden",
            !isChatbot
        );

        securityWorkspace.classList.toggle(
            "hidden",
            isChatbot
        );


        /* Breadcrumb */

        workspaceTitle.textContent =
            isChatbot
                ? "Chatbot"
                : "Security Analyzer";
    }


    /* Product switch */

    switchOptions.forEach(option => {

        option.addEventListener("click", () => {

            switchWorkspace(
                option.dataset.workspace
            );

        });

    });


    /* Initial state */

    switchWorkspace("chatbot");

});