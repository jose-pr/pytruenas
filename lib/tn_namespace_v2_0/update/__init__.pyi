
from pytruenas import Namespace, TrueNASClient
import typing
class Update(Namespace):
    _namespace:typing.Literal['update']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def check_available(self, 
        update_check_available:'UpdateCheckAvailable'={},
    /) -> None: 
        """
        Checks if there is an update available from update server.
        
        status:
          - REBOOT_REQUIRED: an update has already been applied
          - AVAILABLE: an update is available
          - UNAVAILABLE: no update available
          - HA_UNAVAILABLE: HA is non-functional

        Parameters
        ----------
        update_check_available:
            update-check-available
        Returns
        -------
        """
        ...
    @typing.overload
    def download(self, 
    /) -> None: 
        """
        Download updates using selected train.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def file(self, 
        updatefile:'Updatefile'={},
    /) -> None: 
        """
        Updates the system using the uploaded .tar file.
        
        `resume` should be set to `true` if a previous call to this method returned a `CallError` with `errno=EAGAIN`
        meaning that an upgrade can be performed with a warning and that warning is accepted. In that case, re-uploading
        the file is not necessary.
        
        Use null `destination` to create a temporary location.

        Parameters
        ----------
        updatefile:
            updatefile
        Returns
        -------
        """
        ...
    @typing.overload
    def get_auto_download(self, 
    /) -> None: 
        """
        Returns if update auto-download is enabled.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def get_pending(self, 
        path:'str|None'=None,
    /) -> None: 
        """
        Gets a list of packages already downloaded and ready to be applied.
        Each entry of the lists consists of type of operation and name of it, e.g.
        
          {
            "operation": "upgrade",
            "name": "baseos-11.0 -> baseos-11.1"
          }

        Parameters
        ----------
        path:
            path
        Returns
        -------
        """
        ...
    @typing.overload
    def get_trains(self, 
    /) -> None: 
        """
        Returns available trains dict and the currently configured train as well as the
        train of currently booted environment.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def manual(self, 
        path:'str',
        options:'Options'={},
    /) -> None: 
        """
        Update the system using a manual update file.
        
        `path` must be the absolute path to the update file.
        
        `options.resume` should be set to `true` if a previous call to this method returned a `CallError` with
        `errno=EAGAIN` meaning that an upgrade can be performed with a warning and that warning is accepted.
        
        If `options.cleanup` is set to `false` then the manual update file won't be removed on update success and
        newly created BE won't be removed on update failure (useful for debugging purposes).

        Parameters
        ----------
        path:
            `path` must be the absolute path to the update file.
        options:
            options
        Returns
        -------
        """
        ...
    @typing.overload
    def set_auto_download(self, 
        autocheck:'bool',
    /) -> None: 
        """
        Sets if update auto-download is enabled.

        Parameters
        ----------
        autocheck:
            autocheck
        Returns
        -------
        """
        ...
    @typing.overload
    def set_train(self, 
        train:'str',
    /) -> None: 
        """
        Set an update train to be used by default in updates.

        Parameters
        ----------
        train:
            train
        Returns
        -------
        """
        ...
    @typing.overload
    def update(self, 
        update:'Update'={},
    /) -> None: 
        """
        Downloads (if not already in cache) and apply an update.
        
        `resume` should be set to `true` if a previous call to this method returned a `CallError` with `errno=EAGAIN`
        meaning that an upgrade can be performed with a warning and that warning is accepted. In that case, update
        process will be continued using an already downloaded file without performing any extra checks.

        Parameters
        ----------
        update:
            update
        Returns
        -------
        """
        ...

class UpdateCheckAvailable(typing.TypedDict):
        train:'str'
        ...
class Updatefile(typing.TypedDict):
        resume:'bool'
        destination:'typing.Optional[str]'
        ...
class Options(typing.TypedDict):
        dataset_name:'typing.Optional[str]'
        resume:'bool'
        cleanup:'bool'
        ...
class Update(typing.TypedDict):
        dataset_name:'typing.Optional[str]'
        resume:'bool'
        train:'typing.Optional[str]'
        reboot:'bool'
        ...
