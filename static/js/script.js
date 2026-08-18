document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("assessmentForm");

    if (!form) return;

    const steps = Array.from(document.querySelectorAll(".step"));
    const nextBtn = document.getElementById("nextBtn");
    const prevBtn = document.getElementById("prevBtn");
    const progressBar = document.getElementById("progressBar");
    const stepLabel = document.getElementById("stepLabel");
    const progressPercent = document.getElementById("progressPercent");

    let currentStep = 0;

    function showStep(index) {
        currentStep = Math.max(0, Math.min(steps.length - 1, index));

        steps.forEach(function (step, i) {
            step.classList.toggle("active", i === currentStep);
        });

        const percent = Math.round(
            ((currentStep + 1) / steps.length) * 100
        );

        stepLabel.textContent =
            "Step " + (currentStep + 1) + " of " + steps.length;

        progressPercent.textContent = percent + "%";

        progressBar.style.width = percent + "%";

        prevBtn.disabled = currentStep === 0;

       if (currentStep === steps.length - 1) {
    nextBtn.textContent = "Analyze My Career 🚀";
    nextBtn.type = "submit";
} else {
    nextBtn.textContent = "Continue →";
    nextBtn.type = "button";
}

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    }

    function validateStep() {

        // STEP 1 — BASIC PROFILE
        if (currentStep === 0) {
            const requiredFields = steps[0].querySelectorAll(
                "input[required], select[required]"
            );

            for (const field of requiredFields) {
                if (!field.value.trim()) {
                    field.reportValidity();
                    return false;
                }
            }

            return true;
        }

        // STEP 2 — MARKS
        if (currentStep === 1) {

            const stream = document.getElementById("stream").value;

            if (!stream) {
                alert("Please select your academic stream first.");
                return false;
            }

            const activePanel = document.querySelector(
                '.subject-panel[data-stream="' + stream + '"]'
            );

            if (!activePanel) {
                alert("Subjects could not be loaded.");
                return false;
            }

            const markInputs = activePanel.querySelectorAll(
                'input[type="number"]'
            );

            for (const input of markInputs) {

                if (input.value.trim() === "") {
                    alert("Please enter marks for all your subjects.");
                    input.focus();
                    return false;
                }

                const mark = Number(input.value);

                if (isNaN(mark) || mark < 0 || mark > 100) {
                    alert("Marks must be between 0 and 100.");
                    input.focus();
                    return false;
                }
            }

            return true;
        }

        // STEP 3 — INTERESTS
        if (currentStep === 2) {

            const interests = document.querySelectorAll(
                'input[name="interests"]:checked'
            );

            if (interests.length === 0) {
                alert("Please select at least one interest.");
                return false;
            }

            return true;
        }

        // STEP 4 — SKILLS
        if (currentStep === 3) {

            const skills = document.querySelectorAll(
                'input[name="skills"]:checked'
            );

            if (skills.length === 0) {
                alert("Please select at least one skill.");
                return false;
            }

            return true;
        }

        // STEP 5 — CAREER PREFERENCES
        if (currentStep === 4) {

            const ratingRows = steps[4].querySelectorAll(".rating-row");

            for (const row of ratingRows) {

                const selected = row.querySelector(
                    'input[type="radio"]:checked'
                );

                if (!selected) {
                    alert(
                        "Please answer all career preference questions."
                    );
                    row.scrollIntoView({
                        behavior: "smooth",
                        block: "center"
                    });
                    return false;
                }
            }

            return true;
        }

        // STEP 6 — APTITUDE
        if (currentStep === 5) {

            const questions = steps[5].querySelectorAll("fieldset");

            for (const question of questions) {

                const selected = question.querySelector(
                    'input[type="radio"]:checked'
                );

                if (!selected) {
                    alert(
                        "Please answer all assessment questions."
                    );

                    question.scrollIntoView({
                        behavior: "smooth",
                        block: "center"
                    });

                    return false;
                }
            }

            return true;
        }

        return true;
    }

    // NEXT / ANALYZE BUTTON
 nextBtn.addEventListener("click", function (event) {

    if (!validateStep()) {
        event.preventDefault();
        return;
    }

    if (currentStep !== steps.length - 1) {
        event.preventDefault();
        showStep(currentStep + 1);
    }

    // Last step par kuch prevent nahi karenge.
    // Button type="submit" hai, isliye form automatically
    // POST /analyze par submit hoga.
});

    // BACK BUTTON
    prevBtn.addEventListener("click", function () {

        if (currentStep > 0) {
            showStep(currentStep - 1);
        }
    });

    // STREAM / SUBJECTS
    const stream = document.getElementById("stream");

    const subjectPanels = Array.from(
        document.querySelectorAll(".subject-panel")
    );

    function updateSubjects() {

        subjectPanels.forEach(function (panel) {

            if (panel.dataset.stream === stream.value) {
                panel.classList.add("active");
            } else {
                panel.classList.remove("active");
            }

        });
    }

    if (stream) {
        stream.addEventListener("change", updateSubjects);
    }

    updateSubjects();

    showStep(0);
});
