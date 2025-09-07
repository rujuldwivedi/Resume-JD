\ProvidesClass{resume}[2025/08/24 v1.0 Resume class - FAANG safe]
\LoadClass[11pt,letterpaper]{article} % Font size and paper type
\usepackage[parfill]{parskip}
\usepackage{array}
\usepackage{xcolor}
\definecolor{myPurple}{RGB}{0,0,238} % true purple hex #800080
\usepackage[colorlinks=true,
             linkcolor=myPurple,
             urlcolor=myPurple,
             citecolor=myPurple,
             filecolor=myPurple]{hyperref}
\pagestyle{empty} % Suppress page numbers
\def \name#1{\def\@name{#1}}
\def \@name {}
\def \addressSep { | } % Use pipe separator for FAANG style
\let \@addressone \relax
\let \@addresstwo \relax
\let \@addressthree \relax
\def \address #1{
  \@ifundefined{@addresstwo}{
    \def \@addresstwo {#1}
  }{
  \@ifundefined{@addressthree}{
  \def \@addressthree {#1}
  }{
    \def \@addressone {#1}
  }}
}
\def \printaddress #1{
  \begingroup
    \def \\ {\addressSep\ }
    \centerline{#1}
  \endgroup
  \par
  \addressskip
}
\def \printname {
  \begingroup
    \hfil{\MakeUppercase{\namesize\bf \@name}}\hfil
    \nameskip\break
  \endgroup
}
\let\ori@document=\document
\renewcommand{\document}{
  \ori@document
  \printname
  \@ifundefined{@addressone}{}{ \printaddress{\@addressone}}
  \@ifundefined{@addresstwo}{}{ \printaddress{\@addresstwo}}
  \@ifundefined{@addressthree}{}{ \printaddress{\@addressthree}}
}
\newenvironment{rSection}[1]{
  \sectionskip
  \MakeUppercase{{\bf #1}}
  \sectionlineskip
  \hrule
  \begin{list}{}{
    \setlength{\leftmargin}{0em}
  }
  \item[]
}{
  \end{list}
}
\newenvironment{rSubsection}[4]{
 {\bf #1} \hfill {#2}
 \ifthenelse{\equal{#3}{}}{}{
  \\
  {\em #3} \hfill {\em #4}}
  \smallskip
  \begin{list}{$\cdot$}{\leftmargin=0em}
    \itemsep -0.5em \vspace{-0.5em}
  }{
  \end{list}
  \vspace{0.5em}
}
\def\namesize{\LARGE}
\def\addressskip{\smallskip}
\def\sectionlineskip{\medskip}
\def\nameskip{\medskip}
\def\sectionskip{\medskip}