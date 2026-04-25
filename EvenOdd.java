import javax.swing.ImageIcon;
import javax.swing.JOptionPane;

public class Main {
    public static void main(String[] args) {
        String input = JOptionPane.showInputDialog(
                null,
                "Введите целое число",
                "Проверка числа",
                JOptionPane.QUESTION_MESSAGE
        );

        if (input == null) { // нажали Cancel или закрыли окно
            JOptionPane.showMessageDialog(null, "Ввод отменён", "Выход", JOptionPane.INFORMATION_MESSAGE);
            return;
        }

        int number;
        try {
            number = Integer.parseInt(input.trim()); // проверка, что введено целое
        } catch (NumberFormatException e) {
            JOptionPane.showMessageDialog(null, "Вы не ввели целое число", "Ошибка ввода", JOptionPane.ERROR_MESSAGE);
            return;
        }

        boolean even = number % 2 == 0;
        String imgPath = even ? "d:/books/pictures/even.png" : "d:/books/pictures/odd.png";
        ImageIcon img = new ImageIcon(imgPath);

        String txt = even ? "Число " + number + " - четное" : "Число " + number + " - нечетное";
        String title = even ? "Четное число" : "Нечетное число";

        JOptionPane.showMessageDialog(null, txt, title, JOptionPane.PLAIN_MESSAGE, img);
    }
}