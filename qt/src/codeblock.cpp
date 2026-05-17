#include "codeblock.h"
#include <QPainter>
#include <QPalette>
#include <QApplication>
#include <QClipboard>
#include <QMouseEvent>
#include <QDebug>

CodeBlock::CodeBlock(const QString &code, const QString &language, QWidget *parent)
    : QWidget(parent), code(code), language(language)
{
    lineCount = code.count('\n') + 1;
    setMinimumHeight(50 + lineCount * 20);
    setMaximumHeight(400);
    setStyleSheet("background-color: #1E1E1E; border: 1px solid #333333; border-radius: 5px;");
}

CodeBlock::~CodeBlock()
{
}

void CodeBlock::paintEvent(QPaintEvent *event)
{
    QPainter painter(this);
    painter.fillRect(rect(), QColor("#1E1E1E"));
    painter.drawRect(0, 0, width() - 1, height() - 1);
    painter.setPen(QColor("#333333"));

    // Header
    painter.fillRect(0, 0, width(), 30, QColor("#222222"));
    painter.setPen(QColor("#E0E0E0"));
    painter.setFont(QFont("Courier New", 9));
    painter.drawText(10, 20, language.toUpper());

    // Copy button hint
    painter.setPen(QColor("#666666"));
    painter.setFont(QFont("Arial", 8));
    painter.drawText(width() - 120, 20, "Double-click to copy");

    // Code
    painter.setPen(QColor("#FFFFFF"));
    painter.setFont(QFont("Courier New", 10));

    QStringList lines = code.split('\n');
    int y = 50;

    for (int i = 0; i < lines.size(); ++i) {
        // Line number
        painter.setPen(QColor("#666666"));
        painter.setFont(QFont("Courier New", 9));
        painter.drawText(5, y + 15, QString::number(i + 1).rightJustified(3, ' '));

        // Code
        painter.setPen(QColor("#FFFFFF"));
        painter.setFont(QFont("Courier New", 10));
        painter.drawText(50, y + 15, lines[i]);

        y += 20;
    }
}

void CodeBlock::mouseDoubleClickEvent(QMouseEvent *event)
{
    Q_UNUSED(event);
    copyToClipboard();
}

void CodeBlock::copyToClipboard()
{
    QClipboard *clipboard = QApplication::clipboard();
    clipboard->setText(code);
    qDebug() << "Code copied to clipboard";
}

QString CodeBlock::highlightSyntax(const QString &code)
{
    // Basic syntax highlighting
    return code;
}
