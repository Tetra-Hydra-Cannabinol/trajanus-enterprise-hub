// Trajanus Enterprise Hub - Navigation

document.addEventListener('DOMContentLoaded', function() {
    // Add click handling for toolkit cards
    const toolkitCards = document.querySelectorAll('.toolkit-card');

    toolkitCards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Add visual feedback
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = '';
            }, 100);
        });
    });
});

// Navigation utility functions
const Navigation = {
    goHome: function() {
        window.location.href = '../index.html';
    },

    goToToolkit: function(toolkit) {
        const validToolkits = ['pm', 'traffic', 'developer', 'qcm'];
        if (validToolkits.includes(toolkit)) {
            window.location.href = `toolkits/${toolkit}.html`;
        }
    }
};
