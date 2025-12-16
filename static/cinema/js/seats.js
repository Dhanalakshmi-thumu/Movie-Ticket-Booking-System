// let selectedSeats = [];

// document.addEventListener("DOMContentLoaded", () => {
//     const seats = document.querySelectorAll(".seat:not(.booked)");
//     const seatInput = document.getElementById("seatInput");
//     const totalAmount = document.getElementById("totalAmount");

//     seats.forEach(seat => {
//         seat.addEventListener("click", () => {
//             const seatNo = seat.dataset.seat;
//             const price = seat.classList.contains("gold") ? 350 : 250;

//             if (seat.classList.contains("selected")) {
//                 seat.classList.remove("selected");
//                 // Remove seat from selectedSeats array
//                 selectedSeats = selectedSeats.filter(s => s.seatNo !== seatNo);
//             } else {
//                 seat.classList.add("selected");
//                 // Add seat with its price
//                 selectedSeats.push({ seatNo, price });
//             }

//             // Update hidden input with selected seat numbers
//             seatInput.value = selectedSeats.map(s => s.seatNo).join(",");

//             // Calculate total dynamically
//             const total = selectedSeats.reduce((sum, s) => sum + s.price, 0);
//             totalAmount.innerText = total;
//         });
//     });
// });
