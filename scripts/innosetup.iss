; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

; NOTE: the base directory is the one where the script resides and not
; the directory the tool is calling it from
; hence the ..\build\xxxx to fall down to the base directory

; Default values
; #define MyAppName "appname"
; #define MyAppVersion "version"
; #define MyAppPublisher "author"
; #define MyAppYear "year"
; #define MyAppURL "url"
; #define MyAppExeName "appexe"
; #define MyBuildDir "..\build\inno"
; #define MyDistDir "..\dist\inno"
; #define MyAppId "myappid"

#define MyAppName "appname"
#define MyAppVersion "version"
#define MyAppPublisher "author"
#define MyAppYear "year"
#define MyAppURL "url"
#define MyAppExeName "appexe"
#define MyBuildDir "..\build\inno"
#define MyDistDir "..\dist\inno"
#define MyAppId "myappid"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
; The fist { is needed as an escape character
AppId={#MyAppName}-{#MyAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
LicenseFile={#MyBuildDir}\LICENSE
;InfoBeforeFile={#MyBuildDir}\README.md
OutputBaseFilename={#MyAppName}-{#MyAppVersion}-setup
Compression=lzma2/Ultra64
SolidCompression=false
OutputDir={#MyDistDir}
AppVerName={#MyAppVersion}
InternalCompressLevel=Ultra64
ShowLanguageDialog=no
AppCopyright=Copyright (C) {#MyAppYear} {#MyAppPublisher}
; SetupIconFile={#MyBuildDir}\icons\{#MyAppName}.ico
; For updates
UsePreviousAppDir=yes
CreateUninstallRegKey=no
UpdateUninstallLogAppName=false

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}";
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1

[Files]
Source: {#MyBuildDir}\*; DestDir: {app}; Flags: ignoreversion recursesubdirs createallsubdirs uninsremovereadonly;
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:ProgramOnTheWeb,{#MyAppName}}"; Filename: "{#MyAppURL}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, "&", "&&")}}"; Flags: nowait postinstall skipifsilent

[CustomMessages]

[InnoIDE_Settings]
UseRelativePaths=true

[Registry]
root: HKCU; subkey: Software\{#MyAppName}; valuedata: ""; Flags: UninsDeleteKey; valuetype: none;
root: HKCU; subkey: Software\{#MyAppName}\{#MyAppName}; valuedata: ""; Flags: UninsDeleteKey; valuetype: none;
