#include "sysinc.h"
#include "qtinc.h"
#include "brainfuck.h"
#include "mainwindow.h"
#include "globals.h"

enum class CommandType { ADD, SUB, INC, DEC, PUT, GET, BRO, BRC };

class Command {
public:
    CommandType type;
    size_t matchingBracket;

    Command(CommandType t) : type(t), matchingBracket(0) {}
};

class Cell {
private:
    int value;

public:
    Cell() : value(0) {}

    void increment() {
        if (value == 255) {
            value = 0;
        } else {
            value++;
        }
    }

    void decrement() {
        if (value == 0) {
            value = 255;
        } else {
            value--;
        }
    }

    int getValue() const {
        return value;
    }

    void setValue(int newValue) {
        value = newValue;
    }
};

class BrainfuckInterpreter {
private:
    size_t currentCell;
    std::vector<Cell> cells;
    std::vector<std::unique_ptr<CellBox>> cellBoxes;
    MainWindow* mainWindow;
    bool stop;

    static const std::unordered_map<char, CommandType> commandTable;

    void output(char c) {
        std::cout << c;
        QString s = c;
        mainWindow->getTerminalEdit()->moveCursor(QTextCursor::End);
        mainWindow->getTerminalEdit()->textCursor().insertText(s);
    }

    int getInput() {
        mainWindow->getInputEdit()->setReadOnly(false);
        QString s;
        QEventLoop loop;
        QObject::connect(mainWindow->getInputEdit(), SIGNAL(editingFinished()), &loop, SLOT(quit()));
        loop.exec();

        int ret = static_cast<int>(mainWindow->getInputEdit()->text().at(0).toLatin1());
        mainWindow->getInputEdit()->setReadOnly(true);
        mainWindow->getInputEdit()->clear();
        return ret;
    }

    void clearCells() {
        for (auto& cellBox : cellBoxes) {
            cellBox->hide();
        }
        cellBoxes.clear();
    }

    int execute(std::vector<Command>& commands, size_t index);

public:
    BrainfuckInterpreter(MainWindow* mw) : currentCell(0), mainWindow(mw), stop(false) {
        cells.resize(currentCell + 1);
    }

    void executeAll(std::vector<Command>& commands);
    std::vector<Command> parse(const std::string& code);
};

const std::unordered_map<char, CommandType> BrainfuckInterpreter::commandTable = {
    {'+', CommandType::ADD},
    {'-', CommandType::SUB},
    {'>', CommandType::INC},
    {'<', CommandType::DEC},
    {'[', CommandType::BRO},
    {']', CommandType::BRC},
    {'.', CommandType::PUT},
    {',', CommandType::GET}
};

void BrainfuckInterpreter::executeAll(std::vector<Command>& commands) {
    stop = false;
    clearCells();
    size_t i = 0;

    mainWindow->getTerminalEdit()->clear();
    mainWindow->getButtonExec()->setEnabled(false);
    mainWindow->getButtonStop()->setEnabled(true);

    while (i < commands.size() && !stop) {
        std::cout << "Executed " << i;
        i = execute(commands, i);

        if (i < 0) {
            mainWindow->getStatusBar()->showMessage("Error executing code.");
            break;
        }
    }

    mainWindow->getButtonExec()->setEnabled(true);
    mainWindow->getButtonStop()->setEnabled(false);
}

int BrainfuckInterpreter::execute(std::vector<Command>& commands, size_t index) {
    Command& command = commands[index];
    int* currentVal = &cells[currentCell].getValue();
    bool br = false;

    if (!cellBoxes.size()) {
        cellBoxes.push_back(std::make_unique<CellBox>(0, mainWindow->getIndexLayout(), mainWindow->getValueLayout()));
    }

    switch (command.type) {
        case CommandType::ADD:
            cells[currentCell].increment();
            cellBoxes[currentCell]->setValue(cells[currentCell].getValue());
            break;

        case CommandType::SUB:
            cells[currentCell].decrement();
            cellBoxes[currentCell]->setValue(cells[currentCell].getValue());
            break;

        case CommandType::INC:
            if (currentCell == cells.size() - 1) {
                cells.resize(cells.size() + 1);
                cellBoxes.push_back(std::make_unique<CellBox>(currentCell + 1, mainWindow->getIndexLayout(), mainWindow->getValueLayout()));
            }
            currentCell++;
            break;

        case CommandType::DEC:
            if (currentCell != 0) {
                currentCell--;
            }
            break;

        case CommandType::PUT:
            output(static_cast<char>(*currentVal));
            break;

        case CommandType::GET:
            *currentVal = getInput();
            cellBoxes[currentCell]->setValue(*currentVal);
            break;

        case CommandType::BRO:
            br = true;
            if (*currentVal == 0) {
                return command.matchingBracket + 1;
            } else {
                return index + 1;
            }
            break;

        case CommandType::BRC:
            br = true;
            if (*currentVal == 0) {
                return index + 1;
            } else {
                return command.matchingBracket + 1;
            }
            break;

        default:
            return -1;
    }

    if (!br) {
        return index + 1;
    }
    return -1;
}

std::vector<Command> BrainfuckInterpreter::parse(const std::string& code) {
    std::vector<Command> commands;
    std::vector<size_t> brackets;

    for (char& c : code) {
        Command command(commandTable.at(c));
        commands.push_back(command);

        switch (c) {
            case '[':
                brackets.push_back(commands.size() - 1);
                break;

            case ']':
                if (brackets.size() == 0) {
                    throw(BrMismatch);
                } else {
                    commands[commands.size() - 1].matchingBracket = brackets.back();
                    brackets.pop_back();
                    commands[commands[commands.size() - 1].matchingBracket].matchingBracket = commands.size() - 1;
                }
                break;

            default:
                break;
        }
    }

    return commands;
}
